User guide
~~~~~~~~~~

Authentication in the admin backend
===================================

As a content-editor, you should be able to connect to the administration
interface with the credentials and link that your administrator sent you. If
they haven't, please email them with a request and eventually a link to
:doc:`administration`.

Managing representative positions
=================================

Our dear representatives make promises to be elected. These can be submitted by
visitors on the front-end so one of your tasks is to review them and publish
them if they are appropriate.

In "Positions -> Position -> Change" (url should be
``/admin/positions/position/``), above the list table, click the "Published"
select box and choose the "Published: No" option, then click "Search".
Alternatively, you may bookmark
``/admin/positions/position/?published__exact=0``.

Click a "Position" and if it's appropriate then check the "Published" checkbox
and click "Save". The position will now appear in the representative detail
page.

Managing vote recommendations
=============================

A recommendation represents the vote we want representatives to make on a
proposal: representatives doing the "recommended" vote will have their score
increased, others will have their score decreased. Some recommendations may be
more important than others, you can change the number of score points a
recommendation is worth by changing its "weight" (must be a positive integer).

In "Votes -> Recommendations -> Change" (url should be
``/admin/votes/recommendation/``), you can create, update or remove
recommendations.

Your change won't be visible on score as soon as you make it.

Data updates
============

Data updates daily:

- representatives details are updated daily,
- dossiers are synchronised daily,
- proposals are synchronised daily, when proposals are synchronised, they
  become available to use in "Recommendations".
- votes and scores are synchronised daily for proposals which have a
  "Recommendation",

This means that if a proposal arrives today in the database, you may add a
recommendation for it. The next day, votes will be imported and scores will be
updated as well.
