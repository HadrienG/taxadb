#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw


db = pw.Proxy()


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
    parent_taxid = pw.IntegerField(null=False)
    tax_name = pw.CharField()
    lineage_level = pw.CharField()


class Sequence(BaseModel):
    """table Sequence. Each row is a sequence. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='sequences')
    accession = pw.CharField(null=False)
