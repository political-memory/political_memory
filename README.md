[![Build Status](https://travis-ci.org/political-memory/political_memory.svg?branch=master)](https://travis-ci.org/political-memory/political_memory)
[![codecov.io](https://codecov.io/github/political-memory/political_memory/coverage.svg?branch=master)](https://codecov.io/github/political-memory/political_memory?branch=master)

    git clone git@github.com:political-memory/political_memory.git

    cd political_memory

    # Create a throwable virtualenv
    virtualenv ve
    source ve/bin/activate

    # Install python requirements
    pip install -r requirements.txt

    # Create the local db
    python manage.py migrate

    # Install browser libs
    bin/install_client_deps.sh

    # In another terminal (don't forget to activate the venv)
    ./manage.py runserver
