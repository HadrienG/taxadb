#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from peewee import *
import peewee as pw


db = pw.SqliteDatabase('test.sqlite')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Taxa(BaseModel):
    primary = pw.PrimaryKeyField()
    ncbi_taxid = pw.IntegerField(null=False)
    parent_taxid = pw.ForeignKeyField(rel_model=pw.Model)
    tax_name = pw.CharField()
    lineage_level = pw.CharField()


class Sequence(BaseModel):
    primary = pw.PrimaryKeyField()
    taxon_id = pw.ForeignKeyField(Taxa, to_field='primary')
    accession = pw.CharField(null=False)
    version = pw.IntegerField(null=False)
    gi = pw.CharField()
    db_type = pw.CharField(null=False)  # or ForeignKeyField for a table?


def create_db(db):
    db.connect()
    db.create_table(Taxa)
    db.create_table(Sequence)


def parse_node(node_file):
    node_data = list()
    with open(node_file, 'r') as f:
        for line in f:
            line_lst = line.rstrip('\t').split('|')

            data_dict = {
                'ncbi_taxid': line_lst[0],
                'parent_taxid': line_lst[1],
                'tax_name': '',
                'lineage_level': line_lst[2]}
            node_data.append(data_dict)

        with db.atomic():
            for i in range(0, len(node_data), 500):
                Taxa.insert_many(node_data[i:i+500]).execute()
            print('%s rows added' % (len(node_data)))
        db.close()


def main():
    create_db(db)
    parse_node("nodes.dmp")


if __name__ == '__main__':
    main()
