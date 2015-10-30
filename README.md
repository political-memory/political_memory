    git clone git@github.com:political-memory/political_memory.git

    cd political_memory

    virtualenv ve
    source ve/bin/activate

    pip install -r requirements.txt

    python manage.py migrate
