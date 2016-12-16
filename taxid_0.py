#! /usr/bin/env python

import sys
import os
from taxadb import accession
from taxadb.schema import *

TAXADB_DIR = '/data/sqlite3'
TAXADB_DBNAME = 'taxadb'

sqlite = os.path.join(TAXADB_DIR, TAXADB_DBNAME + '_full.sqlite')
postgres = TAXADB_DBNAME
accessions = ['AAA00056', 'AAA00059', 'AAA00053']
print("Query Gss table ...")
taxids = accession.taxid(accessions, postgres, Prot, user='tuco', password='tucobell')
for tax in taxids:
    print(tax)
print("Query Prot table ...")
taxids = accession.lineage_id(accessions, sqlite, Prot, user='tuco', password='tucobell')
for tax in taxids:
    print(tax)
sys.exit(0)
