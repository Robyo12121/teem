from os.path import abspath, dirname, join

from setuptools import find_packages, setup

from teem import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

    
setup(
    name='teem',
    version = __version__,
    description = 'A command line program to interact with Teem in Python',
    long_description= long_description,
    url = None,
    author = 'Robin Staunton-Collins',
    author_email = 'robinstauntoncollins@gmail.com',
    license = 'GNU GPLv3',
    classifiers= [
        'Indended Audience :: Users',
        'Topic :: Utilities',
        'Licence :: GNU GPLv3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    keywords ='cli',
    packages = find_packages(exclude=['docs', 'test*']),
    install_requires = ['requests', 'oauthlib', 'requests_oauth']
    entry_points = {
        'console_scripts': [
            'teem=teem.cli:main',
            ],
        },
)
