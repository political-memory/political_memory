API Documentation
~~~~~~~~~~~~~~~~~

Memopol publishes its data with a read-only REST API using `Django REST
Framework <http://www.django-rest-framework.org/>`_.  The API is browseable and
partially self-documented, from the ``/api`` URL.

The goal of this documentation is to plug the holes in the
automatically-generated documentation.

Overview
========

The API homepage resides at the ``/api/`` URL. Each model is accessible from two
URLs:

* ``/api/<model>/`` for a (filterable) list of objects
* ``/api/<model>/<pk>/`` to get a detailed view of a specific object

When accessing the API from a web browser, data should be displayed in a
user-friendly paginated interface, and relation fields are links to the
corresponding API URLs (if that's not the case, you can force it by appending
``format=api`` to the querystring).  To get raw JSON data instead, either pass
an ``Accept: application/json`` request header or append ``format=json`` to the
querystring.

Object lists may be filtered using ``field=value`` in the querystring ; related
fields may be used in filters with double underscores (for example
``representative__name=John``).  Alternative operators may be available for
some fields (for example ``score__gte=100``), amongst which:

* ``lte``: matches values that are lower than or equal to the specified value
* ``gte``: matches values greater than equal to or the specified value
* ``icontains``: matches values that contain the specified value, ignoring case

Note that fields that are made available for filtering depend on each model;
the same goes for alternative operators (by default only exact match is
available).

Finally, note that this documentation does not show the data schema.  Feel free
to browse the API yourself to find out how data is published.

Representatives API
===================

This API provides views on representatives and mandates.

Representatives
---------------

The ``/api/representatives/[<pk>/]`` endpoints give access to representatives.
The following fields are available for filtering:

* ``active``: True or False
* ``slug`` (alt.: icontains)
* ``id``
* ``remote_id``
* ``first_name``
* ``last_name`` (alt.: icontains)
* ``gender``: M or F
* ``birth_place``
* ``birth_date`` (alt.: gte, lte)
* ``search``: searches in the ``first_name``, ``last_name`` and ``slug`` fields

Mandates
--------

The ``/api/mandates/[<pk>/]`` endpoints give access to mandates. The following
fields are available for filtering:

* ``id``
* ``group__name`` (alt.: icontains)
* ``group__abbreviation``
* ``search``: searches in the ``group__name`` and ``group_abbreviation`` fields

Constituency
------------

The ``/api/constituencies/[<pk>/]`` endpoints give access to constituencies.

Groups
------

The ``/api/groups/[<pk>/]`` endpoints give access to groups.

Representatives-votes API
=========================

This API provides views on dossiers, proposals and votes.

Dossiers
--------

The ``/api/dossiers/[<pk>/]`` endpoints give access to dossiers. The following
fields are available for filtering:

* ``fingerprint``
* ``title`` (alt.: icontains)
* ``reference`` (alt.: icontains)
* ``search``: searches in the ``fingerprint``, ``title``, ``reference``,
  ``text`` and ``proposals__title`` fields

Proposals
---------

The ``/api/proposals/[<pk>/]`` endpoints give access to proposals. The following
fields are available for filtering:

* ``fingerprint``
* ``dossier__fingerprint``
* ``title`` (alt.: icontains)
* ``description`` (alt.: icontains)
* ``reference`` (alt.: icontains)
* ``datetime`` (alt.: gte, lte)
* ``kind``
* ``search``: searches in the ``fingerprint``, ``title``,
  ``dossier__fingerprint``, ``dossier__title`` and ``dossier__reference`` fields

Votes
-----

The ``/api/votes/[<pk>/]`` endpoints give access to votes. The following fields
are available for filtering:

* ``proposal__fingerprint``
* ``position``
* ``representative_name`` (alt.: icontains)
* ``representative``


Memopol API
===========

This API provides views on recommendations and representative scores.

Recommendations
---------------

The ``/api/recommendations/[<pk>/]`` endpoints give access to recommendations.
The following fields are available for filtering:

* ``id``
* ``recommendation``
* ``title`` (alt.: icontains)
* ``description`` (alt.: icontains)
* ``weight`` (alt.: gte, lte)
* ``search``: searches in the ``title`` and ``description`` fields

Scored Votes
------------

The ``/api/scored_votes/[<pk>/]`` endpoints give access to scored votes; that
is, representative votes with their contribution to the representative score.
Only votes that match a recommendation are visible using this endpoint.  The
following fields are available for filtering:

* ``representative``
* ``proposal``
* ``proposal__dossier``

Dossier Scores
--------------

The ``/api/dossier_scores/[<pk>/]`` endpoints give access to dossier scores;
that is, the contribution of each dossier on a representative score. Only
dossiers with recommendations are visible using this endpoint.  The following
fields are available for filtering:

* ``dossier``
* ``representative``
* ``score`` (alt.: gte, lte)

Representative scores
---------------------

The ``/api/scores/[<pk>/]`` endpoints give access to total scores for each
representative. The following fields are available for filtering:

* ``representative``
* ``score`` (alt.: gte, lte)
