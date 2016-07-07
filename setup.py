from setuptools import find_packages, setup

setup(
    name='django-representatives',
    version='0.0.28',
    description='Base app for government representative',
    author='Laurent Peuch, Olivier Le Thanh Duong, Yohan Boniface, Arnaud Fabre, James Pic, Nicolas Joyard',
    author_email='webmaster@memopol.org',
    url='http://github.com/political-memory/django-representatives',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    keywords='django government parliament',
    install_requires=[
        'django>=1.8,<1.9',
        'ijson>=2,<3',
    ],
    extras_require={
        'celery': 'celery',
        'api': [
            'django-filter>=0.13,<0.14',
            'djangorestframework>=3,<4',
        ],
        'testing': [
            'codecov>=2,<3',
            'flake8>=2,<3',
            'pep8>=1,<2',
            'pytest>=2,<3',
            'pytest-django>=2,<3',
            'pytest-cov>=2,<3',
            'django-responsediff>=0.6,<0.7'
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
