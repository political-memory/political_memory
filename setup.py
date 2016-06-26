from setuptools import setup

setup(name='political-memory',
    version='0.0.1',
    description='OpenShift App',
    packages=['political_memory'],
    package_dir={'political_memory': '.'},
    author='James Pic, Laurent Peuch, Arnaud Fabre, Nicolas Joyard',
    author_email='cortex@worlddomination.be',
    url='http://github.com/political-memory/political_memory/',
    install_requires=[
        'django-autocomplete-light>=3.0,<4.0',
        'django-bootstrap3>=6,<7',
        'django-coffeescript>=0.7,<0.8',
        'django-compressor>=1,<2',
        'django-datetime-widget>=0.9,<1.0',
        'django-filter>=0.13,<0.14',
        'django-libsass>=0.7,<0.8',
        'django-representatives-votes==0.0.17',
        'django-representatives==0.0.25',
        'django-taggit>=0.17,<0.18',
        'django>=1.8,<1.9',
        'djangorestframework>=3,<4',
        'hamlpy>=0.82,<0.83',
        'ijson>=2.2,<2.3',
        'python-dateutil>=2.4,<2.5',
        'unicodecsv>=0.14,<0.15',
        'pytz',  # Always use up-to-date TZ data
        'django-suit>=0.2,<0.3',
        'sqlparse>=0.1,<0.2',
        'psycopg2>=2,<3',
    ],
    extras_require={
        # Full version hardcode for testing dependencies so that
        # tests don't break on master without any obvious reason.
        'testing': [
            'codecov>=2,<3',
            'flake8>=2,<3',
            'django-responsediff>=0.6,<0.7',
            'pep8>=1,<2',
            'pytest>=2,<3',
            'pytest-django>=2,<3',
            'pytest-cov>=2,<3',
        ]
    },
    entry_points={
        'console_scripts': [
            'memopol_import_positions = representatives_positions.contrib.import_positions:main',  # noqa
            'memopol_import_recommendations = representatives_recommendations.contrib.import_recommendations:main',  # noqa
        ]
    }
)
