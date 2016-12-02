#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import *


def taxid(acc_number, db_name, table):
    """given an acession number, returns his taxid"""
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    with db.atomic():
        taxid = table.get(table.accession == acc_number)
    db.close()
    return taxid
