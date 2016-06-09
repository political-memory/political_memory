from setuptools import find_packages, setup

setup(
    name='django-representatives-votes',
    version='0.0.16',
    description='Base app for government representative votes',
    author='Olivier Le Thanh Duong, Laurent Peuch, Arnaud Fabre, James Pic, Nicolas Joyard',
    author_email='olivier@lethanh.be',
    url='http://github.com/political-memory/django-representatives-votes',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    keywords='django government parliament votes',
    install_requires=[
        'django-representatives>=0.0.15',
        'py-dateutil',
        'pytz',
        'ijson',
    ],
    extras_require={
        'api': [
            'django-filter',
            'djangorestframework',
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
