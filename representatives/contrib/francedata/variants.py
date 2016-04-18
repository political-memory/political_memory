# coding: utf-8

# Equivalences of nat. Assembly committees
_equiv_Com_AN = {
}

# Abbreviations for nat. Assembly committees
_abbr_Com_AN = {
    (u"Commission chargée de l'application de l'article 26 de la "
        u"constitution"): "AnComImmu",
    u"Commission de la défense nationale et des forces armées": "AnComDef",
    u"Commission des affaires culturelles et de l'éducation": "AnComCult",
    u"Commission des affaires économiques": "AnComEco",
    u"Commission des affaires étrangères": "AnComEtrg",
    u"Commission des affaires européennes": "AnComEU",
    u"Commission des affaires sociales": "AnComSoc",
    (u"Commission des finances, de l'économie générale et du contrôle "
        u"budgétaire"): "AnComFin",
    (u"Commission des lois constitutionnelles, de la législation et de "
        u"l'administration générale de la république"): "AnComLois",
    u"Commission du développement durable et de l'aménagement du territoire":
        "AnComDevD"
}

# Equivalences of nat. Assembly delegations
_equiv_Deleg_AN = {
}

# Abbreviations for nat. Assembly delegations
_abbr_Deleg_AN = {
}

# Equivalences of Senate committees
_equiv_Com_SEN = {
    u"COMMISSION DES AFFAIRES EUROPÉENNES Commission des affaires européennes":
        u"Commission des affaires européennes",
    u"Commission de l'aménagement du territoire et du développement durable":
        (u"Commission du développement durable, des infrastructures, de "
            u"l'équipement et de l'aménagement du territoire")
}

# Abbreviations for Senate committees
_abbr_Com_SEN = {
    u"Commission de la culture, de l'éducation et de la communication":
        "SenComCult",
    u"Commission des affaires économiques": "SenComEco",
    u"Commission des affaires étrangères, de la défense et des forces armées":
        "SenComDef",
    u"Commission des affaires européennes": "SenComEU",
    u"Commission des affaires sociales": "SenComSoc",
    (u"Commission des finances, du contrôle budgétaire et des comptes "
        u"économiques de la nation"): "SenComFin",
    (u"Commission des lois constitutionnelles, de législation, du suffrage "
        u"universel, du Règlement et d'administration générale"): "SenComLois",
    (u"Commission du développement durable, des infrastructures, de "
        u"l'équipement et de l'aménagement du territoire"): "SenComDevD",
    u"Commission sénatoriale pour le contrôle de l'application des lois":
        "SenComAppL"
}

# Equivalences of Senate delegations
_equiv_Deleg_SEN = {
}

# Abbreviations for Senate delegations
_abbr_Deleg_SEN = {
}


def _get_rep_district_name(data):
    num = data.get('num_circo')
    nom = data.get('nom_circo')

    if num == 'nd':
        return nom
    else:
        ordinal = u'ère' if num == 1 else u'ème'
        return '%s (%d%s circonscription)' % (nom, num, ordinal)


def _get_sen_comittees(data):
    comittees = []
    start = data['mandat_debut']

    for g in data['responsabilites']:
        orga = g['responsabilite']['organisme']
        role = g['responsabilite']['fonction']

        if not orga.lower().startswith('commission'):
            continue

        if orga in _equiv_Com_SEN:
            orga = _equiv_Com_SEN[orga]

        comittees.append({
            'abbr': _abbr_Com_SEN[orga] if orga in _abbr_Com_SEN else '',
            'name': orga,
            'role': role,
            'start': start
        })

    return comittees


def _get_sen_delegations(data):
    delegations = []
    start = data['mandat_debut']

    for g in ([i['responsabilite'] for i in data['responsabilites']] +
            [j['responsabilite'] for j in data['groupes_parlementaires']]):
        orga = g['organisme']
        role = g['fonction']

        if orga.lower().startswith('commission'):
            continue

        if orga in _equiv_Deleg_SEN:
            orga = _equiv_Deleg_SEN[orga]

        delegations.append({
            'abbr': _abbr_Deleg_SEN[orga] if orga in _abbr_Deleg_SEN else '',
            'name': orga,
            'role': role,
            'start': start
        })

    return delegations


def _get_an_comittees(data):
    comittees = []
    start = data['mandat_debut']

    for g in data['responsabilites']:
        orga = g['responsabilite']['organisme']
        role = g['responsabilite']['fonction']

        if not orga.lower().startswith('commission'):
            continue

        if orga in _equiv_Com_AN:
            orga = _equiv_Com_AN[orga]

        comittees.append({
            'abbr': _abbr_Com_AN[orga] if orga in _abbr_Com_AN else '',
            'name': orga,
            'role': role,
            'start': start
        })

    return comittees


def _get_an_delegations(data):
    delegations = []
    start = data['mandat_debut']

    for g in ([i['responsabilite'] for i in data['responsabilites']] +
            [j['responsabilite'] for j in data['groupes_parlementaires']]):
        orga = g['organisme']
        role = g['fonction']

        if orga.lower().startswith('commission'):
            continue

        if orga in _equiv_Deleg_AN:
            orga = _equiv_Deleg_AN[orga]

        delegations.append({
            'abbr': _abbr_Deleg_AN[orga] if orga in _abbr_Deleg_AN else '',
            'name': orga,
            'role': role,
            'start': start
        })

    return delegations


#
# Variant configuration
# - mail_domain is used to distinguish official vs personal emails
# - off_* fields are used for the official address of meps
# - mandates defines how mandates are created from the rep json
#
# Mandates are defined as follows
# - 'kind' indicates the group kind, a constant string
# - 'chamber' tells whether the group belongs to the chamber
# - 'from', if present, must be a function that takes the rep json and returns
#   an array of dicts; one group will be created from each item in the dict.
#   When 'from' is not present, only one group wil be created using the rep
#   json (IOW, 'from' defaults to lambda repjson: [repjson])
# - 'name', 'abbr', 'role', 'start', 'end' are strings that are interpolated
#   against the rep json or items returned by 'from'.
# - 'name_path', 'abbr_path', etc. can replace 'name', 'abbr'... by specifying
#   a slash-separated dictionnary path where the value is to be found in the
#   rep json or item returned by 'from'
# - 'name_fn', 'abbr_fn', etc. can also replace 'name', 'abbr'... by a
#   function that takes the input item (rep json or item returned by 'from')
#   and returns the value
#
FranceDataVariants = {
    "AN": {
        "chamber": u"Assemblée nationale",
        "abbreviation": "AN",
        "remote_id_field": "url_an",
        "mail_domain": "@assemblee-nationale.fr",
        "off_city": "Paris",
        "off_street": u"Rue de l'Université",
        "off_number": "126",
        "off_code": "75355",
        "off_name": u"Assemblée nationale",
        "mandates": [
            {
                "kind": "chamber",
                "chamber": True,
                "abbr": "AN",
                "name": u"Assemblée nationale",
                "role": u"Député",
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "group",
                "chamber": True,
                "abbr": "%(groupe_sigle)s",
                "name_path": "groupe/organisme",
                "role_path": "groupe/fonction",
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "department",
                "abbr": "%(num_deptmt)s",
                "name": "%(nom_circo)s",
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "district",
                "abbr": "%(num_deptmt)s-%(num_circo)s",
                "name_fn": _get_rep_district_name,
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "committee",
                "chamber": True,
                "from": _get_an_comittees,
                "abbr": "%(abbr)s",
                "name": "%(name)s",
                "role": "%(role)s",
                "start": "%(start)s"
            },
            {
                "kind": "delegation",
                "chamber": True,
                "from": _get_an_delegations,
                "abbr": "%(abbr)s",
                "name": "%(name)s",
                "role": "%(role)s",
                "start": "%(start)s"
            }
        ]
    },

    "SEN": {
        "chamber": u"Sénat",
        "abbreviation": "SEN",
        "remote_id_field": "url_institution",
        "mail_domain": "@senat.fr",
        "off_city": "Paris",
        "off_street": u"Rue de Vaugirard",
        "off_number": "15",
        "off_code": "75291",
        "off_name": u"Palais du Luxembourg",
        "mandates": [
            {
                "kind": "chamber",
                "chamber": True,
                "abbr": "SEN",
                "name": u"Sénat",
                "role": u"Sénateur",
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "group",
                "chamber": True,
                "abbr": "%(groupe_sigle)s",
                "name_path": "groupe/organisme",
                "role_path": "groupe/fonction",
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "department",
                "abbr": "%(num_deptmt)s",
                "name": "%(nom_circo)s",
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "district",
                "abbr": "%(num_deptmt)s-%(num_circo)s",
                "name_fn": _get_rep_district_name,
                "start": "%(mandat_debut)s"
            },
            {
                "kind": "committee",
                "chamber": True,
                "from": _get_sen_comittees,
                "abbr": "%(abbr)s",
                "name": "%(name)s",
                "role": "%(role)s",
                "start": "%(start)s"
            },
            {
                "kind": "delegation",
                "chamber": True,
                "from": _get_sen_delegations,
                "abbr": "%(abbr)s",
                "name": "%(name)s",
                "role": "%(role)s",
                "start": "%(start)s"
            }
        ]
    }
}
