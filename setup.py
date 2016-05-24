from setuptools import find_packages, setup

setup(
    name='django-representatives',
    version='0.0.19',
    description='Base app for government representative',
    author='Laurent Peuch, Olivier Le Thanh Duong, Yohan Boniface, Arnaud Fabre, James Pic, Nicolas Joyard',
    author_email='webmaster@memopol.org',
    url='http://github.com/political-memory/django-representatives',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    keywords='django government parliament',
    install_requires=[
        'ijson',
    ],
    extras_require={
        'celery': 'celery',
        'api': [
            'django-filter',
            'djangorestframework',
        ]
    },
    entry_points={
        'console_scripts': [
            'parltrack_import_representatives = representatives.contrib.parltrack.import_representatives:main',
            'francedata_import_representatives = representatives.contrib.francedata.import_representatives:main',
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
