#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='taxadb',
    version='0.5.0',

    description='locally query the ncbi taxonomy',

    url='https://github.com/HadrienG/taxadb',
    download_url='https://github.com/HadrienG/taxadb/tarball/0.5.0',
    author='Hadrien Gourlé, Juliette Hayer, Emmanuel Quevillon',
    author_email='hadrien.gourle@slu.se, juliette.hayer@slu.se,\
        tuco@pasteur.fr',

    license='MIT',
    packages=find_packages(exclude=['tests']),

    install_requires=['ftputil', 'peewee==2.8.1', 'nose', 'nose-testconfig'],
    # Allow PostgreSQL and MySQL as option
    extras_require={
        'postgres': ["psycopg2>=2.6.2"],
        'mysql': ["PyMySQL>=0.7.10"],
    },

    entry_points={
        'console_scripts': ['taxadb = taxadb.app:main'],
    }
)
