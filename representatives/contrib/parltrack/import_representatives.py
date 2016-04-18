# coding: utf-8

import logging
import sys
from datetime import datetime

import django.dispatch
import ijson
import django
from django.apps import apps
from django.db import transaction
from django.template.defaultfilters import slugify
from django.utils import timezone

from representatives.models import (Address, Constituency, Country, Email,
                                    Group, Mandate, Phone, Representative,
                                    WebSite, Chamber)

logger = logging.getLogger(__name__)

representative_pre_import = django.dispatch.Signal(
    providing_args=['representative_data'])


def _parse_date(date):
    return datetime.strptime(date, "%Y-%m-%dT00:%H:00").date()


class GenericImporter(object):

    def pre_import(self):
        self.import_start_datetime = timezone.now()

    def post_import(self):
        # Clean not touched models
        models = [Representative, Group, Constituency,
                  Mandate, Address, Phone, Email, WebSite]
        for model in models:
            model.objects.filter(
                updated__lt=self.import_start_datetime).delete()

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


class ParltrackImporter(GenericImporter):
    url = 'http://parltrack.euwiki.org/dumps/ep_meps_current.json.xz'
    check_etag = True

    def parse_date(self, date):
        return _parse_date(date)

    def __init__(self):
        self.cache = {
            'countries': {c.name: c.pk for c in Country.objects.all()},
        }
        self.ep_chamber, _ = Chamber.objects.get_or_create(
            name='European Parliament', abbreviation='EP')
        self.ep_constituency, _ = Constituency.objects.get_or_create(
            name='European Parliament')
        self.ep_group, _ = Group.objects.get_or_create(
            name='European Parliament', kind='chamber', abbreviation='EP',
            chamber=self.ep_chamber)

    @transaction.atomic
    def manage_mep(self, mep_json):
        '''
        Import a mep as a representative from the json dict fetched from
        parltrack
        '''
        remote_id = mep_json['UserID']

        if not remote_id:
            logger.warning('Skipping MEP without UID %s %s',
                           mep_json['Name']['full'], mep_json['UserID'])
            return

        # Some versions of memopol will connect to this and skip inactive meps.
        responses = representative_pre_import.send(sender=self,
                representative_data=mep_json)

        for receiver, response in responses:
            if response is False:
                logger.debug(
                    'Skipping MEP %s', mep_json['Name']['full'])
                return

        try:
            representative = Representative.objects.get(remote_id=remote_id)
        except Representative.DoesNotExist:
            representative = Representative(remote_id=remote_id)

        # Save representative attributes
        self.import_representative_details(representative, mep_json)

        representative.save()

        self.add_mandates(representative, mep_json)

        self.add_contacts(representative, mep_json)

        logger.debug('Imported MEP %s', unicode(representative))

        return representative

    def import_representative_details(self, representative, mep_json):
        representative.active = mep_json['active']

        if mep_json.get("Birth"):
            representative.birth_date = _parse_date(mep_json["Birth"]["date"])
            if "place" in mep_json["Birth"]:
                representative.birth_place = mep_json["Birth"]["place"]

        representative.first_name = mep_json["Name"]["sur"]
        representative.last_name = mep_json["Name"]["family"]
        representative.full_name = mep_json["Name"]["full"]

        representative.photo = mep_json["Photo"]

        fix_last_name_with_prefix = {
            "Esther de LANGE": "de LANGE",
            "Patricia van der KAMMEN": "van der KAMMEN",
            "Judith A. MERKIES": "MERKIES",
            "Heinz K. BECKER": "BECKER",
            "Cornelis de JONG": "de JONG",
            "Peter van DALEN": "van DALEN",
            "Sophia in 't VELD": "in 't VELD",
            "Marielle de SARNEZ": "de SARNEZ",
            "Anne E. JENSEN": "JENSEN",
            "Wim van de CAMP": "van de CAMP",
            "Lambert van NISTELROOIJ": "van NISTELROOIJ",
            "Johannes Cornelis van BAALEN": "van BAALEN",
            "Ioannis A. TSOUKALAS": "TSOUKALAS",
            "Pilar del CASTILLO VERA": "del CASTILLO VERA",
            "Luis de GRANDES PASCUAL": "de GRANDES PASCUAL",
            "Philippe de VILLIERS": "de VILLIERS",
            "Daniël van der STOEP": "van der STOEP",
            "William (The Earl of) DARTMOUTH": "(The Earl of) Dartmouth",
            "Bairbre de BRÚN": u'de Br\xfan',
            "Karl von WOGAU": u'von WOGAU',
            "Ieke van den BURG": u'van den BURG',
            "Manuel António dos SANTOS": u'dos SANTOS',
            "Paul van BUITENEN": u'van BUITENEN',
            "Elly de GROEN-KOUWENHOVEN": u'de GROEN-KOUWENHOVEN',
            "Margrietus van den BERG": u'van den BERG',
            u'Dani\xebl van der STOEP': u'van der STOEP',
            "Alexander Graf LAMBSDORFF": u'Graf LAMBSDORFF',
            u'Bairbre de BR\xdaN': u'de BR\xdaN',
            'Luigi de MAGISTRIS': 'de MAGISTRIS',
        }

        if fix_last_name_with_prefix.get(representative.full_name):
            representative.last_name = fix_last_name_with_prefix[
                representative.full_name]
        elif representative.last_name == "J.A.J. STASSEN":
            representative.last_name_with_prefix = "STASSEN"

        gender_convertion_dict = {
            u"F": 1,
            u"M": 2
        }
        if 'Gender' in mep_json:
            representative.gender = gender_convertion_dict.get(mep_json[
                                                               'Gender'], 0)
        else:
            representative.gender = 0

        representative.cv = "\n".join(
            [cv_title for cv_title in mep_json.get("CV", [])])

        representative.slug = slugify(
            representative.full_name if representative.full_name
            else representative.first_name + " " + representative.last_name
        )

    def add_mandates(self, representative, mep_json):
        def create_mandate(mandate_data, representative, group, constituency):
            if mandate_data.get("start"):
                begin_date = _parse_date(mandate_data.get("start"))
            if mandate_data.get("end"):
                end_date = _parse_date(mandate_data.get("end"))

            role = mandate_data['role'] if 'role' in mandate_data else ''
            mandate, _ = Mandate.objects.get_or_create(
                representative=representative,
                group=group,
                constituency=constituency,
                role=role,
                begin_date=begin_date,
                end_date=end_date
            )

            if _:
                logger.debug('Created mandate %s with %s', mandate.pk,
                             mandate_data)

        # Committee
        for mandate_data in mep_json.get('Committees', []):
            if mandate_data.get("committee_id"):
                group, _ = self.touch_model(model=Group,
                        abbreviation=mandate_data['committee_id'],
                        kind='committee', name=mandate_data['Organization'],
                        chamber=self.ep_chamber)

                create_mandate(mandate_data, representative, group,
                               self.ep_constituency)

        # Delegations
        for mandate_data in mep_json.get('Delegations', []):
            group, _ = self.touch_model(model=Group,
                                        kind='delegation',
                                        name=mandate_data['Organization'],
                                        chamber=self.ep_chamber
                                        )

            create_mandate(mandate_data, representative, group,
                           self.ep_constituency)

        # Group
        convert = {
            "S&D": "SD",
            "NA": "NI",
            "ID": "IND/DEM",
            "PPE": "EPP",
            "Verts/ALE": "Greens/EFA"}
        for mandate_data in mep_json.get('Groups', []):
            if not mandate_data.get('groupid'):
                continue

            if isinstance(mandate_data.get('groupid'), list):
                abbreviation = mandate_data.get('groupid')[0]
            else:
                abbreviation = mandate_data.get('groupid')

            abbreviation = convert.get(abbreviation, abbreviation)
            group, _ = self.touch_model(model=Group,
                                        abbreviation=abbreviation,
                                        kind='group',
                                        name=mandate_data['Organization'],
                                        chamber=self.ep_chamber
                                        )

            create_mandate(mandate_data, representative, group,
                           self.ep_constituency)

        # Countries
        for mandate_data in mep_json.get('Constituencies', []):
            if not mandate_data:
                continue

            _country = Country.objects.get(name=mandate_data['country'])

            group, _ = self.touch_model(model=Group,
                                        abbreviation=_country.code,
                                        kind='country',
                                        name=_country.name
                                        )

            local_party = mandate_data['party'] if mandate_data[
                'party'] and mandate_data['party'] != '-' else 'unknown'

            country_id = (self.cache['countries'].get(mandate_data['country'])
                if 'country' in mandate_data else None)

            save_constituency = False
            try:
                constituency = Constituency.objects.get(name=local_party)
            except Constituency.DoesNotExist:
                constituency = Constituency(name=local_party)
                save_constituency = True

            if constituency.country_id != country_id:
                constituency.country_id = country_id
                save_constituency = True

            if save_constituency:
                constituency.save()

            create_mandate(mandate_data, representative, group, constituency)

            create_mandate(mandate_data, representative, self.ep_group,
                           self.ep_constituency)

        # Organisations
        for mandate_data in mep_json.get('Staff', []):

            group, _ = self.touch_model(model=Group,
                                        abbreviation='',
                                        kind='organization',
                                        name=mandate_data['Organization']
                                        )

            create_mandate(mandate_data, representative, group,
                           self.ep_constituency)

    def add_contacts(self, representative, mep_json):
        # Addresses
        if mep_json.get('Addresses', None):
            address = mep_json.get('Addresses')

            belgium = Country.objects.get(name="Belgium")
            france = Country.objects.get(name="France")

            for city in address:
                if city in ['Brussels', 'Strasbourg']:
                    if city == 'Brussels':
                        country = belgium
                        street = u"rue Wiertz / Wiertzstraat"
                        number = '60'
                        postcode = '1047'
                        name = "Brussels European Parliament"
                    elif city == 'Strasbourg':
                        country = france
                        street = u"Av. du Président Robert Schuman - CS 91024"
                        number = '1'
                        postcode = '67070'
                        name = "Strasbourg European Parliament"

                    address_model, _ = self.touch_model(model=Address,
                        representative=representative, country=country,
                        city=city,
                        floor=address[city]['Address']['Office'][:3],
                        office_number=address[city]['Address']['Office'][3:],
                        street=street, number=number, postcode=postcode,
                        kind='official', name=name)

                    self.touch_model(model=Phone,
                        representative=representative, address=address_model,
                        kind='office phone',
                        number=address[city].get('Phone', ''))

        # Emails
        if mep_json.get('Mail', None):
            mails = mep_json.get('Mail')
            if not isinstance(mails, list):
                mails = list(mails)

            for mail in mails:
                self.touch_model(
                    model=Email,
                    representative=representative,
                    kind=('official' if '@europarl.europa.eu' in mail
                        else 'other'),
                    email=mail)
        # WebSite
        websites = mep_json.get('Homepage', [])
        for url in websites:
            self.touch_model(model=WebSite,
                             url=url,
                             representative=representative
                             )

        if mep_json.get('Twitter', None):
            self.touch_model(model=WebSite,
                             representative=representative,
                             kind='twitter',
                             url=mep_json.get('Twitter')[0]
                             )

        if mep_json.get('Facebook', None):
            self.touch_model(model=WebSite,
                             representative=representative,
                             kind='facebook',
                             url=mep_json.get('Facebook')[0]
                             )


def main(stream=None):
    if not apps.ready:
        django.setup()

    importer = ParltrackImporter()
    GenericImporter.pre_import(importer)

    for data in ijson.items(stream or sys.stdin, 'item'):
        importer.manage_mep(data)
    # Commenting for now, it's a bit dangerous, if a json file was corrupt it
    # would drop valid data !
    # importer.post_import()
