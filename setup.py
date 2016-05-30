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
        'django-bootstrap3>=6.2,<6.3',
        'django-coffeescript>=0.7,<0.8',
        'django-compressor>=1.6,<1.7',
        'django-datetime-widget>=0.9,<1.0',
        'django-filter>=0.11,<0.12',
        'django-representatives-votes==0.0.15',
        'django-representatives==0.0.21',
        'django-taggit>=0.17,<0.18',
        'django>=1.8,<1.9',
        'djangorestframework>=3.2.0,<3.3.0',
        'hamlpy>=0.82,<0.83',
        'ijson>=2.2,<2.3',
        'lesscpy>=0.10.2,<0.11.0',
        'python-dateutil>=2.4,<2.5',
        'unicodecsv==0.14.1',
        'pytz==2015.7',
        'django-suit>=0.2.16,<0.3.0',
        'sqlparse>=0.1',
    ],
    extras_require={
        # Full version hardcode for testing dependencies so that
        # tests don't break on master without any obvious reason.
        'testing': [
            'django-responsediff==0.2.0',
            'flake8==2.5.1',
            'pep8==1.5.7',
            'pytest==2.8.5',
            'pytest-django==2.9.1',
            'pytest-cov==2.2.0',
            'codecov',
        ]
    },
    entry_points={
        'console_scripts': [
            'memopol_import_positions = representatives_positions.contrib.import_positions:main',  # noqa
            'memopol_import_recommendations = representatives_recommendations.contrib.import_recommendations:main',  # noqa
        ]
    }
)
