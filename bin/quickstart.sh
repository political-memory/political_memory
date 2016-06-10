#!/bin/bash

#
# Quick-start script for new developers
# Usage: from repo root, `source bin/quickstart.sh`
#

set -e

REPOROOT=$(dirname $(dirname $0))

# Ensure we're at the root of the memopol repository
pushd $REPOROOT >/dev/null

# Create & activate python virtual environment
virtualenv memopol_env
source memopol_env/bin/activate

# Install python dependencies
pip install -e .[testing]

# Install client dependencies
bin/install_client_deps.sh

# Setup environment
export DJANGO_DEBUG=True
export DJANGO_SETTINGS_MODULE=memopol.settings

# Run django migration to create database
./manage.py migrate

# Import sample data
./manage.py loaddata memopol/fixtures/smaller_sample.json

echo
echo "You're all set!"
echo "To start the application run the following from the repository root ($REPOROOT):"
echo "  source memopol_env/bin/activate"
echo "  export DJANGO_DEBUG=True DJANGO_SETTINGS_MODULE=memopol.settings"
echo "  ./manage.py runserver"
echo
echo "If you make changes, don't forget to run tests using:"
echo "  flake8 . --exclude '*/migrations,docs,static' --ignore E128"
echo "  py.test memopol representatives_positions representatives_recommendations"
echo
echo "Happy hacking ;)"
echo

popd >/dev/null
