#!/usr/bin/env python
# -*- coding: utf-8 -*-

import taxa_db
from peewee import *


def parse_node(node_file):

    with open(node_file, 'r') as f:
        for line in f:
            line_lst = line.rstrip('\t').split('|')
            print(line_lst)
            taxid = line_lst[0]
            parent_id = line_lst[1]
            rank = line_lst[2]

            cur_tax = Taxa.create(ncbi_taxid=taxid, parent_taxid=parent_id, tax_name='', lineage_level=rank)
            break
    # uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
    # uncle_bob.save() # bob is now stored in the database
    # grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)

def main():
    db = SqliteDatabase('test.sqlite')
    db.connect()
    parse_node("data/nodes.dmp")

if __name__ == '__main__':
    main()
