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
    ncbi_taxid -- the TaxID of the taxon (from nodes.dmp)
    parent_taxid -- the TaxID of the parent taxon (from nodes.dmp)
    tax_name -- the scientific name of the taxon (from names.dmp)
    lineage_level -- the level of lineage of the taxon (from nodes.dmp)
    """
    ncbi_taxid = pw.IntegerField(null=False, index=True, primary_key=True)
    parent_taxid = pw.IntegerField(null=False)
    tax_name = pw.CharField()
    lineage_level = pw.CharField()


class Est(BaseModel):
    """table Est. Each row is a sequence from nucl_est. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='est')
    accession = pw.CharField(null=False, index=True)


class Gb(BaseModel):
    """table Gb. Each row is a sequence from nucl_gb. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='gb')
    accession = pw.CharField(null=False, index=True)


class Gss(BaseModel):
    """table Gss. Each row is a sequence from nucl_gss. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='gss')
    accession = pw.CharField(null=False, index=True)


class Wgs(BaseModel):
    """table Wgs. Each row is a sequence from nucl_wgs. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='wgs')
    accession = pw.CharField(null=False, index=True)


class Prot(BaseModel):
    """table prot. Each row is a sequence from prot. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    primary = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='prot')
    accession = pw.CharField(null=False, index=True)
