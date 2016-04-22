# coding: utf-8

import logging
import sys
from datetime import datetime

import django.dispatch
import ijson
import django
from django.apps import apps
from django.db import transaction
from django.utils import timezone

from representatives.models import (Country, Mandate, Email, Address, WebSite,
                                    Representative, Constituency, Phone, Group,
                                    Chamber)
from variants import FranceDataVariants


logger = logging.getLogger(__name__)

representative_pre_import = django.dispatch.Signal(
    providing_args=['representative_data'])


def _get_mdef_item(mdef, item, json, default=None):
    if item in mdef:
        try:
            return mdef[item] % json
        except:
            return default

    if '%s_path' % item in mdef:
        return _get_path(json, mdef['%s_path' % item])

    if '%s_fn' % item in mdef:
        return mdef['%s_fn' % item](json)

    return default


def _parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d").date()


def _create_mandate(representative, group, constituency, role='',
                    begin_date=None, end_date=None):
    mandate, _ = Mandate.objects.get_or_create(
        representative=representative,
        group=group,
        constituency=constituency,
        role=role,
        begin_date=begin_date,
        end_date=end_date
    )

    if _:
        logger.debug('Created mandate %s', mandate.pk)


def _get_path(dict_, path):
    '''
    Get value at specific path in dictionary. Path is specified by slash-
    separated string, eg _get_path(foo, 'bar/baz') returns foo['bar']['baz']
    '''
    cur = dict_
    for part in path.split('/'):
        cur = cur[part]
    return cur


class GenericImporter(object):

    def pre_import(self):
        self.import_start_datetime = timezone.now()

    def touch_model(self, model, **data):
        '''
        This method create or look up a model with the given data
        it saves the given model if it exists, updating its
        updated field
        '''

        instance, created = model.objects.get_or_create(**data)

        if not created:
            if instance.updated < self.import_start_datetime:
                instance.save()     # Updates updated field

        return (instance, created)


class FranceDataImporter(GenericImporter):
    url = 'http://francedata.future/data/parlementaires.json'

    def parse_date(self, date):
        return _parse_date(date)

    def __init__(self, variant):
        self.france = Country.objects.get(name="France")
        self.variant = FranceDataVariants[variant]
        self.chamber, _ = Chamber.objects.get_or_create(
            name=self.variant['chamber'],
            abbreviation=self.variant['abbreviation'], country=self.france)
        self.ch_constituency, _ = Constituency.objects.get_or_create(
            name=self.variant['chamber'], country=self.france)

    @transaction.atomic
    def manage_rep(self, rep_json):
        '''
        Import a rep as a representative from the json dict fetched from
        FranceData (which comes from nosdeputes.fr)
        '''
        remote_id = rep_json[self.variant['remote_id_field']]

        if rep_json['num_circo'] == 'non disponible':
            rep_json['num_circo'] = 'nd'

        if not remote_id:
            logger.warning('Skipping MEP without UID %s %s',
                           rep_json['nom'],
                           rep_json[self.variant['remote_id_field']])
            return

        # Some versions of memopol will connect to this and skip inactive reps.
        responses = representative_pre_import.send(sender=self,
                representative_data=rep_json)

        for receiver, response in responses:
            if response is False:
                logger.debug(
                    'Skipping MEP %s', rep_json['nom'])
                return

        try:
            representative = Representative.objects.get(remote_id=remote_id)
        except Representative.DoesNotExist:
            representative = Representative(remote_id=remote_id)

        # Save representative attributes
        self.import_representative_details(representative, rep_json)

        representative.save()

        self.add_mandates(representative, rep_json)

        self.add_contacts(representative, rep_json)

        logger.debug('Imported MEP %s', unicode(representative))

        return representative

    def import_representative_details(self, representative, rep_json):
        representative.active = True

        if rep_json.get("date_naissance"):
            representative.birth_date = _parse_date(rep_json["date_naissance"])
        if rep_json.get("lieu_naissance"):
            representative.birth_place = rep_json["lieu_naissance"]

        representative.photo = rep_json['photo_url']
        representative.full_name = rep_json["nom"]

        gender_convertion_dict = {
            u"F": 1,
            u"H": 2
        }
        if 'sexe' in rep_json:
            representative.gender = gender_convertion_dict.get(rep_json[
                                                               'sexe'], 0)
        else:
            representative.gender = 0

        representative.slug = rep_json['slug']

    def add_mandates(self, representative, rep_json):
        '''
        Create mandates from rep data based on variant configuration
        '''

        # Mandate in country group for party constituency
        if rep_json.get('parti_ratt_financier'):
            constituency, _ = Constituency.objects.get_or_create(
                name=rep_json.get('parti_ratt_financier'), country=self.france)

            group, _ = self.touch_model(model=Group,
                                        abbreviation=self.france.code,
                                        kind='country',
                                        name=self.france.name)

            _create_mandate(representative, group, constituency, 'membre')

        # Configurable mandates
        for mdef in self.variant['mandates']:
            if mdef.get('chamber', False):
                chamber = self.chamber
            else:
                chamber = None

            if 'from' in mdef:
                elems = mdef['from'](rep_json)
            else:
                elems = [rep_json]

            for elem in elems:
                name = _get_mdef_item(mdef, 'name', elem, '')
                abbr = _get_mdef_item(mdef, 'abbr', elem, '')

                group, _ = self.touch_model(model=Group,
                                            abbreviation=abbr,
                                            kind=mdef['kind'],
                                            chamber=chamber,
                                            name=name)

                role = _get_mdef_item(mdef, 'role', elem, 'membre')
                start = _get_mdef_item(mdef, 'start', elem, None)
                if start is not None:
                    start = _parse_date(start)
                end = _get_mdef_item(mdef, 'end', elem, None)
                if end is not None:
                    end = _parse_date(end)

                _create_mandate(representative, group, self.ch_constituency,
                                role, start, end)

                logger.debug(
                    '%s => %s: %s of "%s" (%s) %s-%s' % (rep_json['slug'],
                    mdef['kind'], role, name, abbr, start, end))

    def add_contacts(self, representative, rep_json):
        # Websites
        websites = rep_json.get('sites_web', [])
        for site in websites:
            if not site['site'].startswith('http://twitter.com/'):
                self.touch_model(model=WebSite,
                                 url=site['site'],
                                 representative=representative
                                 )

        # Twitter
        if rep_json.get('twitter'):
            tid = rep_json.get('twitter')
            self.touch_model(model=WebSite,
                             representative=representative,
                             kind='twitter',
                             url='http://twitter.com/%s' % tid
                             )

        # E-mails
        emails = rep_json.get('emails', [])
        for email in emails:
            mail = email['email']
            self.touch_model(
                model=Email,
                representative=representative,
                kind=('official' if mail.endswith(self.variant['mail_domain'])
                    else 'other'),
                email=mail)

        # Official address
        off_name = self.variant['off_name']
        official_addr, _ = self.touch_model(model=Address,
                                            representative=representative,
                                            country=self.france,
                                            city=self.variant['off_city'],
                                            street=self.variant['off_street'],
                                            number=self.variant['off_number'],
                                            postcode=self.variant['off_code'],
                                            kind='official',
                                            name=off_name
                                            )

        # Addresses & phone numbers
        addresses = rep_json.get('adresses', [])
        for item in addresses:
            addr = None
            if 'geo' in item:
                props = item['geo'].get('properties', {})
                name = ''

                if item['adresse'].lower().startswith('permanence'):
                    name = 'Permanence'

                addr, _ = self.touch_model(model=Address,
                                           representative=representative,
                                           country=self.france,
                                           city=props.get('city', ''),
                                           street=props.get('street', ''),
                                           number=props.get('housenumber', ''),
                                           postcode=props.get('postcode', ''),
                                           kind='',
                                           name=name
                                           )
            elif item['adresse'].lower().startswith(off_name.lower()):
                addr = official_addr

            if 'tel' in item:
                self.touch_model(model=Phone, address=addr,
                                 representative=representative,
                                 kind='', number=item['tel']
                                 )


def main(stream=None):
    if not apps.ready:
        django.setup()

    an_importer = FranceDataImporter('AN')
    GenericImporter.pre_import(an_importer)

    sen_importer = FranceDataImporter('SEN')
    GenericImporter.pre_import(sen_importer)

    for data in ijson.items(stream or sys.stdin, ''):
        for rep in data:
            if rep['chambre'] == 'AN':
                an_importer.manage_rep(rep)
            elif rep['chambre'] == 'SEN':
                sen_importer.manage_rep(rep)
