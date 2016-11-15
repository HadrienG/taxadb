#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='taxadb',
    version='a2',


    description='taxadb',
    long_descirption=readme,

    url='https://github.com/HadrienG/taxa_db',
    author='Hadrien Gourlé, Juliette Hayer',
    author_email='hadrien.gourle@slu.se, juliette.hayer@slu.se',

    license='MIT',
    packages=find_packages(exclude=['tests']),

    install_requires=['ftputil', 'peewee==2.8.1', 'PyMySQL', 'nose'],

    entry_points={
        'console_scripts': ['taxadb = taxadb.app:main'],
    }
)
