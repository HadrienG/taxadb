#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from taxadb.schema import *

from taxadb import accession


def test_taxid():
    taxids = accession.taxid(
        ['X17276'],
        'taxadb/test/test_db.sqlite',
        Gb)
    for taxon in taxids:
        assert taxon[0] == 'X17276'
        assert taxon[1] == 9646


def test_sci_name():
    sci_name = accession.sci_name(
        ['Z12029'],
        'taxadb/test/test_db.sqlite',
        Gb)
    for taxon in sci_name:
        assert taxon[0] == 'Z12029'
        assert taxon[1] == 'Bos indicus'


def test_lineage_id():
    lineage_id = accession.lineage_id(
        ['X52702'],
        'taxadb/test/test_db.sqlite',
        Gb)
    for taxon in lineage_id:
        assert taxon[0] == 'X52702'
        assert taxon[1] == [
            9771, 9766, 9765, 9761, 9721, 91561, 314145, 1437010, 9347, 32525,
            40674, 32524, 32523, 1338369, 8287, 117571, 117570, 7776, 7742,
            89593, 7711, 33511, 33213, 6072, 33208, 33154, 2759, 131567]


def test_lineage_name():
    lineage_name = accession.lineage_name(
        ['X60065'],
        'taxadb/test/test_db.sqlite',
        Gb)
    for taxon in lineage_name:
        assert taxon[0] == 'X60065'
        print(taxon[1])
        assert taxon[1] == [
            'Bos taurus', 'Bos', 'Bovinae', 'Bovidae', 'Pecora', 'Ruminantia',
            'Cetartiodactyla', 'Laurasiatheria', 'Boreoeutheria', 'Eutheria',
            'Theria', 'Mammalia', 'Amniota', 'Tetrapoda',
            'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi',
            'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Craniata',
            'Chordata', 'Deuterostomia', 'Bilateria', 'Eumetazoa', 'Metazoa',
            'Opisthokonta', 'Eukaryota', 'cellular organisms']
