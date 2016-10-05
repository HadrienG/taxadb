#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
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
    tax_name -- the scientific name of the taxon (from names.dmp)
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
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    version -- the version of the sequence.
    gi -- (deprecated) the GI number of the sequence.
    db_type -- the database where the sequence is from.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, to_field='ncbi_taxid')
    accession = pw.CharField(null=False)
    version = pw.IntegerField(null=False)
    gi = pw.CharField()
    db_type = pw.CharField(null=False)


def create_db(db):
    """Create the database."""
    db.connect()
    db.create_table(Taxa)
    db.create_table(Sequence)


def parse_taxdump(nodes_file, names_file):
    """Parse the nodes.dmp and names.dmp files (from taxdump.tgz) and insert
    taxons in the Taxa table.

    Arguments:
    nodes_file -- the nodes.dmp file
    names_file -- the names.dmp file
    """
    # parse nodes.dmp
    nodes_data = list()
    with open(nodes_file, 'r') as f:
        for line in f:
            line_list = line.split('|')
            data_dict = {
                'ncbi_taxid': line_list[0].strip('\t'),
                'parent_taxid': line_list[1].strip('\t'),
                'tax_name': '',
                'lineage_level': line_list[2].strip('\t')
                }
            nodes_data.append(data_dict)
    print('parsed nodes')

    # parse names.dmp
    names_data = list()
    with open(names_file, 'r') as f:
        for line in f:
            if 'scientific name' in line:
                line_list = line.split('|')
                data_dict = {
                    'ncbi_taxid': line_list[0].strip('\t'),
                    'tax_name': line_list[1].strip('\t')
                    }
                names_data.append(data_dict)
    print('parsed names')

    # merge the two dictionaries
    taxa_info_list = list()
    taxa_info = {}
    for nodes, names in zip(nodes_data, names_data):
        taxa_info = {**nodes, **names}  # PEP 448, requires python 3.5
        taxa_info_list.append(taxa_info)
    print('merge successful')

    # insert in database
    with db.atomic():
        for i in range(0, len(taxa_info_list), 500):
            Taxa.insert_many(taxa_info_list[i:i+500]).execute()
    print('Taxa: completed')


def parse_nucl_gss(nucl_gss):
    """Parse the nucl_gss_accession2taxid file.

    Arguments:
    nucl_gss -- input file (gzipped)
    """
    acc_data = list()
    with gzip.open(nucl_gss, 'rb') as f:
        f.readline()  # discard the header
        for line in f:
            line_list = line.decode().rstrip('\n').split('\t')
            data_dict = {
                'accession': line_list[0],
                'version': line_list[1].split('.')[1],
                'taxid': line_list[2],
                'gi': line_list[3],
                'db_type': 'gss'
            }
            acc_data.append(data_dict)
    print(len(acc_data))

    # insert in database
    with db.atomic():
        for i in range(0, len(acc_data), 500):
            Sequence.insert_many(acc_data[i:i+500]).execute()
            print('%s records added' % (i))


def main():
    create_db(db)
    parse_taxdump('nodes.dmp', 'names.dmp')
    parse_nucl_gss('nucl_gss.accession2taxid.gz')


if __name__ == '__main__':
    main()
