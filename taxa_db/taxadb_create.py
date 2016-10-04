#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from peewee import *
import peewee as pw


db = pw.SqliteDatabase('test.sqlite')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Taxa(BaseModel):
    """table Taxa. Each row is a taxon.

    Fields:
    primary -- the primary key
    ncbi_taxid -- the TaxID of the taxon (from nodes.dmp)
    parent_taxid -- the TaxID of the parent taxon (from nodes.dmp)
    tax_name -- the name of the taxon
    lineage_level -- the level of lineage of the taxon (from nodes.dmp)
    """
    primary = pw.PrimaryKeyField()
    ncbi_taxid = pw.IntegerField(null=False)
    parent_taxid = pw.ForeignKeyField(rel_model=pw.Model)
    tax_name = pw.CharField()
    lineage_level = pw.CharField()


class Sequence(BaseModel):
    """table Sequence. Each row is a sequence. Each sequence has a taxon_id.

    Fields:
    primary -- the primary key
    taxon_id -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    version -- the version of the sequence.
    gi -- (deprecated) the GI number of the sequence.
    db_type -- the database where the sequence is from.
    """
    primary = pw.PrimaryKeyField()
    taxon_id = pw.ForeignKeyField(Taxa, to_field='primary')
    accession = pw.CharField(null=False)
    version = pw.IntegerField(null=False)
    gi = pw.CharField()
    db_type = pw.CharField(null=False)  # or ForeignKeyField for a table?


def create_db(db):
    """Create the database."""
    db.connect()
    db.create_table(Taxa)
    db.create_table(Sequence)


def parse_node(node_file):
    """Parse the node.dmp file (from taxdump.tgz) and insert taxons in the
    Taxa table.

    Arguments:
    node_file -- the node.dmp file"""
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
