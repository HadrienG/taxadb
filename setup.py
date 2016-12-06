#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='taxadb',
    version='0.4a',


    description='locally query the ncbi taxonomy',

    url='https://github.com/HadrienG/taxadb',
    download_url='https://github.com/HadrienG/taxadb/tarball/0.3a',
    author='Hadrien Gourlé, Juliette Hayer',
    author_email='hadrien.gourle@slu.se, juliette.hayer@slu.se',

    license='MIT',
    packages=find_packages(exclude=['tests']),

    install_requires=['ftputil', 'peewee==2.8.1', 'PyMySQL', 'nose'],

    entry_points={
        'console_scripts': ['taxadb = taxadb.app:main'],
    }
)
