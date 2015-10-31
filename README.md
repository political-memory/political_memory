    git clone git@github.com:political-memory/political_memory.git

    cd political_memory

    cp memopol/config.json.sample memopol/config.json

    # Create a throwable virtualenv
    virtualenv ve
    source ve/bin/activate

    # Install python requirements
    pip install -r requirements.txt

    # Create the local db
    python manage.py migrate

    # Some static files
    bower install

    # Install node modules
    npm install

    # Build static files
    node_modules/gulp/bin/gulp.js less

    # In another terminal (don't forget to activate the venv)
    ./manage.py runserver
