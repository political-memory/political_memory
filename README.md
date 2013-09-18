    git clone git@github.com:Psycojoker/django-parltrack-votes.git
    git clone git@github.com:Psycojoker/django-representatives.git
    git clone git@github.com:Psycojoker/yolopol.git

    cd yolopol
    ln -s ../django-parltrack-votes/parltrack_votes/ .
    ln -s ../django-representatives/representatives/ .

    virtualenv ve
    source ve/bin/activate

    pip install -r requirements.txt

    python manage.py syncdb
