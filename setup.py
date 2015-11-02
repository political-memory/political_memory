from setuptools import setup, find_packages

setup(name='political-memory',
    version='0.0.1',
    description='OpenShift App',
    packages=['political_memory'],
    package_dir={'political_memory': '.'},
    author='Laurent Peuch',
    author_email='cortex@worlddomination.be',
    url='http://github.com/political-memory/political_memory/',
    install_requires=[
        'django',
        'django-debug-toolbar',
        'django_pdb',
        'django_extensions',
        'werkzeug',
        'south',
        'hamlpy',
        'django-coffeescript',
        'ijson',
        'python-dateutil',
        'pytz',
    ],
)
