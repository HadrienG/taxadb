#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *


def create_db():
    db = SqliteDatabase('test.sqlite')

    class Lineage(Model):
        primary = PrimaryKeyField()
        level = CharField()

        class Meta:
            database = db

    class Taxa(Model):
        primary = PrimaryKeyField()
        subtaxon_id = ForeignKeyField(rel_model=Model)
        ncbi_taxid = CharField(null=False)
        tax_name = CharField()
        lineage_level = ForeignKeyField(Lineage, to_field='primary')

        class Meta:
            database = db

    class Sequence(Model):
        primary = PrimaryKeyField()
        taxon_id = ForeignKeyField(Taxa, to_field='primary')
        accession = CharField(null=False)
        version = IntegerField(null=False)
        gi = CharField()
        db_type = CharField(null=False)  # or ForeignKeyField for a table?

        class Meta:
            database = db

    db.connect()
    db.create_table(Lineage)
    db.create_table(Taxa)
    db.create_table(Sequence)


if __name__ == '__main__':
    main()
