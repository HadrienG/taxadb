#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *


class Taxa(Model):
    primary = PrimaryKeyField()
    ncbi_taxid = IntegerField(null=False)
    parent_taxid = ForeignKeyField(rel_model=Model)
    tax_name = CharField()
    lineage_level = CharField()


class Sequence(Model):
    primary = PrimaryKeyField()
    taxon_id = ForeignKeyField(Taxa, to_field='primary')
    accession = CharField(null=False)
    version = IntegerField(null=False)
    gi = CharField()
    db_type = CharField(null=False)  # or ForeignKeyField for a table?


def create_db():
    db = SqliteDatabase('test.sqlite')
    db.connect()
    db.create_table(Taxa)
    db.create_table(Sequence)


def main():
    create_db()

if __name__ == '__main__':
    main()
