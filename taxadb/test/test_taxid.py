#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from taxadb import taxid


def test_sci_name():
    name = taxid.sci_name(37572, 'taxadb/test/test_db.sqlite')
    assert name == 'Papilionoidea'


def test_lineage_id():
    lineage = taxid.lineage_id(9986, 'taxadb/test/test_db.sqlite')
    assert lineage == [
        9986, 9984, 9979, 9975, 314147, 314146, 1437010, 9347, 32525, 40674,
        32524, 32523, 1338369, 8287, 117571, 117570, 7776, 7742, 89593, 7711,
        33511, 33213, 6072, 33208, 33154, 2759, 131567]


def test_lineage_name():
    lineage = taxid.lineage_name(37081, 'taxadb/test/test_db.sqlite')
    assert lineage == [
        'Spheniscus magellanicus', 'Spheniscus', 'Spheniscidae',
        'Sphenisciformes', 'Neognathae', 'Aves', 'Coelurosauria',
        'Theropoda', 'Saurischia', 'Dinosauria', 'Archosauria',
        'Archelosauria', 'Sauria', 'Sauropsida', 'Amniota', 'Tetrapoda',
        'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi', 'Teleostomi',
        'Gnathostomata', 'Vertebrata', 'Craniata', 'Chordata', 'Deuterostomia',
        'Bilateria', 'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota',
        'cellular organisms']
