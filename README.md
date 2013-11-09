    git clone git@github.com:political-memory/django-representatives-votes.git
    git clone git@github.com:political-memory/django-representatives.git
    git clone git@github.com:political-memory/political_memory.git

    cd political_memory
    ln -s ../django-representatives-votes/representatives_votes/ .
    ln -s ../django-representatives/representatives/ .

    virtualenv ve
    source ve/bin/activate

    pip install -r requirements.txt

    python manage.py syncdb
    python manage.py migrate
