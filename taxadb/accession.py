#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import *


def taxid(acc_number_list, db_name, table):
    """given a list of acession numbers, returns their associated
    Taxa objects"""
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    with db.atomic():
        taxid = table.select().where(table.accession << acc_number_list)
        # taxid = table.get(table.accession == acc_number)
    db.close()
    return taxid
