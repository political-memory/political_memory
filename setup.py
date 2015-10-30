from setuptools import setup, find_packages


setup(
    name='django-representatives-votes',
    version='0.0.1',
    description='Base app for government representative votes',
    author='Olivier Le Thanh Duong',
    author_email='olivier@lethanh.be',
    url='http://github.com/political-memory/django-representatives-votes',
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3',
    keywords='django government parliament votes',
    classifiers=[
        'Development Status :: 1 - Alpha/Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
