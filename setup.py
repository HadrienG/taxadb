#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from taxadb.version import __version__

url = 'https://github.com/HadrienG/taxadb'

setup(
    name='taxadb',
    version=__version__,

    description='locally query the ncbi taxonomy',

    url=url,
    download_url=url + '/tarball/' + __version__,
    author='Hadrien Gourlé, Juliette Hayer, Emmanuel Quevillon',
    author_email='hadrien.gourle@slu.se, juliette.hayer@slu.se,\
        tuco@pasteur.fr',

    license='MIT',
    packages=find_packages(exclude=['tests']),

    tests_require=['nose', 'nose-testconfig'],
    install_requires=['ftputil', 'peewee==2.8.1'],
    # Allow PostgreSQL and MySQL as option
    extras_require={
        'postgres': ["psycopg2>=2.6.2"],
        'mysql': ["PyMySQL>=0.7.10"],
    },

    entry_points={
        'console_scripts': ['taxadb = taxadb.app:main'],
    }
)
