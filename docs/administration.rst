Administrator guide
~~~~~~~~~~~~~~~~~~~

This guide targets the administrator who has deployed
the website in production.

Authentication in the admin backend
===================================

If you haven't already, create a super-administrator
account with command::

    ./manage.py createsuperuser

Then use this account to authenticate in the
administration backend located in ``/admin``.

User groups
===========

You should create a user group with all permissions
on:

- vote | recommendation
- positions | position

Creating a user
===============

To create a content administrator, create a user with:

- "Staff status": checked, otherwise the user won't be
  able to authenticate in the administration backend,
- groups: at least the group created above.

Then, send the credentials to the user along with a link to :doc:`usage`.
