#!/bin/bash

#
# Quick-start script for new developers
# Usage: from repo root, `source bin/quickstart.sh`
#

set -x

REPOROOT=$(dirname $(dirname $0))

# Ensure we're at the root of the memopol repository
pushd $REPOROOT >/dev/null

# Create & activate python virtual environment
virtualenv memopol_env
source memopol_env/bin/activate

# Install python dependencies
pip install -U pip setuptools
pip install -e .[testing]

# Install client dependencies
src/memopol/bin/install_client_deps.sh

# Create pg user and database
if [ $(psql -c "select 'CNT=' || count(1) from pg_catalog.pg_user where usename='memopol';" -U postgres | grep CNT=1 | wc -l) -lt 1 ]; then
	psql -c "create user memopol with password 'memopol';" -U postgres
fi
psql -c "alter role memopol with createdb;" -U postgres
if [ $(psql -l -U postgres | egrep "^ memopol\W" | wc -l) -lt 1 ]; then
	psql -c "create database memopol with owner memopol;" -U postgres
fi

# Setup environment
export DJANGO_DEBUG=True
export DJANGO_SETTINGS_MODULE=memopol.settings

# Run django migration to create database
memopol migrate

# Import sample data
memopol loaddata data_sample.json

echo
echo "You're all set!"
echo "To start the application run the following from the repository root ($REPOROOT):"
echo "  source memopol_env/bin/activate"
echo "  export DJANGO_DEBUG=True DJANGO_SETTINGS_MODULE=memopol.settings"
echo "  memopol runserver"
echo
echo "If you make changes, don't forget to run tests using:"
echo "  flake8 . --exclude '*/migrations,docs,static' --ignore E128"
echo "  py.test memopol representatives_positions representatives_recommendations"
echo
echo "Happy hacking ;)"
echo

popd >/dev/null
