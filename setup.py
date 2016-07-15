#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(name='taxa_db',
      version='a1',


      description='taxa_db',
      long_descirption=readme,

      url='https://github.com/HadrienG/taxa_db',
      author='Hadrien Gourlé, Juliette Hayer',
      author_email='hadrien.gourle@slu.se, juliette.hayer@slu.se',

      license='GPL3',
      packages=find_packages(exclude=['tests']),

      install_requires=['ftputil', 'peewee', 'nose'])
