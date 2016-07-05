from setuptools import find_packages, setup

setup(
    name='django-representatives-votes',
    version='0.0.18',
    description='Base app for government representative votes',
    author='Olivier Le Thanh Duong, Laurent Peuch, Arnaud Fabre, James Pic, Nicolas Joyard',
    author_email='olivier@lethanh.be',
    url='http://github.com/political-memory/django-representatives-votes',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    keywords='django government parliament votes',
    install_requires=[
        'django>1.8,<1.9',
        'django-representatives>=0.0.27',
        'py-dateutil>=2,<3',
        'ijson>=2,<3',
        'pytz',  # Always use up-to-date TZ data
    ],
    extras_require={
        'api': [
            'django-filter>=0.13,<0.14',
            'djangorestframework>=3,<4',
        ],
        'testing': [
            'codecov>=2,<3',
            'flake8>=2,<3',
            'mock>=2,<3',
            'pep8>=1,<2',
            'pytest>=2,<3',
            'pytest-django>=2,<3',
            'pytest-cov>=2,<3',
            'django-responsediff>=0.6,<0.7'
        ]
    },
    entry_points={
        'console_scripts': [
            'parltrack_import_dossiers = representatives_votes.contrib.parltrack.import_dossiers:main',
            'parltrack_import_votes = representatives_votes.contrib.parltrack.import_votes:main',
            'francedata_import_dossiers = representatives_votes.contrib.francedata.import_dossiers:main',
            'francedata_import_scrutins = representatives_votes.contrib.francedata.import_scrutins:main',
            'francedata_import_votes = representatives_votes.contrib.francedata.import_votes:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
