#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from taxadb.taxadb import TaxaDB
from taxadb.accessionid import AccessionID
from taxadb.taxid import TaxID
from taxadb.schema import Accession, Taxa
from nose.plugins.attrib import attr
from testconfig import config


class TestMainFunc(unittest.TestCase):
    """Class to test global methods"""

    @attr('main')
    def test_max_limit_exceeded(self):
        """Check max length of ids raises an exception"""
        ids = [i for i in range(1, 1001)]
        with self.assertRaises(SystemExit):
            TaxaDB.check_list_ids(ids)

    @attr('main')
    def test_max_limit_ok(self):
        ids = [i for i in range(1, 90)]
        self.assertTrue(TaxaDB.check_list_ids(ids))

    @attr('main')
    def test_wrong_dbtype(self):
        """Check wrong dbtype raises an exception"""
        with self.assertRaises(SystemExit):
            TaxaDB(dbtype='fake')


class TestTaxadb(unittest.TestCase):
    """Main class to test AccessionID and TaxID method with sqlite"""

    def setUp(self):
        # Set attirbutes
        self.dbtype = None
        self.username = None
        self.password = None
        self.hostname = None
        self.port = None
        self.dbname = None

        # If config does not contains key sql, it means no config file passed on command line
        # so we default to sqlite test
        if 'sql' not in config:
            config['sql'] = {'dbtype': 'sqlite', 'dbname': 'taxadb/test/test_db.sqlite'}

        self.dbtype = config['sql']['dbtype']
        # Defaults to sqlite
        if self.dbtype is None or self.dbtype == '':
            self.dbtype = 'sqlite'
        if self.dbtype not in ['postgres', 'mysql', 'sqlite']:
            self.fail("dbtype option %s not supported" % str(self.dbtype))

        self.dbname = config['sql']['dbname']
        # Defaults to sqlite test database
        if self.dbname is None or self.dbname == '':
            self.dbname = 'taxadb/test/test_db.sqlite'

        if 'username' in config['sql'] and config['sql']['username'] is not None:
            self.username = config['sql']['username']
        if 'password' in config['sql'] and config['sql']['password'] is not None:
            self.password = config['sql']['password']
        if 'hostname' in config['sql'] and config['sql']['hostname'] is not None:
            self.hostname = config['sql']['hostname']
        if 'port' in config['sql'] and config['sql']['port']:
            self.port = int(config['sql']['port'])

    def _buildTaxaDBObject(self, obj):
        sql = obj(dbname=self.dbname, dbtype=self.dbtype, username=self.username, password=self.password,
                  hostname=self.hostname, port=self.port)
        return sql

    @attr('main')
    def test_table_exists_ok(self):
        """Check the method return True when checking ofr existsing table"""
        obj = self._buildTaxaDBObject(TaxaDB)
        self.assertTrue(obj.check_table_exists(Accession))
        self.assertTrue(obj.check_table_exists(Taxa))

    @attr('accessionid')
    @attr('main')
    def test_accession_taxid(self):
        """Check the method get the correct taxid for a given accesion id"""
        accession = self._buildTaxaDBObject(AccessionID)
        taxids = accession.taxid(['X17276'])
        for taxon in taxids:
            self.assertEqual(taxon[0], 'X17276')
            self.assertEqual(taxon[1], 9646)

    @attr('accessionid')
    def test_accession_sci_name(self):
        accession = self._buildTaxaDBObject(AccessionID)
        sci_name = accession.sci_name(['Z12029'])
        for taxon in sci_name:
            assert taxon[0] == 'Z12029'
            assert taxon[1] == 'Bos indicus'

    @attr('accessionid')
    def test_accession_lineage_id(self):
        accession = self._buildTaxaDBObject(AccessionID)
        lineage_id = accession.lineage_id(['X52702'])
        for taxon in lineage_id:
            self.assertEqual(taxon[0], 'X52702')
            self.assertListEqual(taxon[1], [
                9771, 9766, 9765, 9761, 9721, 91561, 314145, 1437010, 9347, 32525,
                40674, 32524, 32523, 1338369, 8287, 117571, 117570, 7776, 7742,
                89593, 7711, 33511, 33213, 6072, 33208, 33154, 2759, 131567])

    @attr('accessionid')
    def test_accession_lineage_name(self):
        accession = self._buildTaxaDBObject(AccessionID)
        lineage_name = accession.lineage_name(['X60065'])
        for taxon in lineage_name:
            self.assertEqual(taxon[0], 'X60065')
            self.assertListEqual(taxon[1], [
                'Bos taurus', 'Bos', 'Bovinae', 'Bovidae', 'Pecora', 'Ruminantia',
                'Cetartiodactyla', 'Laurasiatheria', 'Boreoeutheria', 'Eutheria',
                'Theria', 'Mammalia', 'Amniota', 'Tetrapoda',
                'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi',
                'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Craniata',
                'Chordata', 'Deuterostomia', 'Bilateria', 'Eumetazoa', 'Metazoa',
                'Opisthokonta', 'Eukaryota', 'cellular organisms'])

    @attr('taxid')
    def test_taxid_sci_name(self):
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.sci_name(37572)
        self.assertEqual(name, 'Papilionoidea')

    @attr('taxid')
    def test_taxid_lineage_id(self):
        taxid = self._buildTaxaDBObject(TaxID)
        lineage = taxid.lineage_id(9986)
        self.assertListEqual(lineage, [
            9986, 9984, 9979, 9975, 314147, 314146, 1437010, 9347, 32525, 40674,
            32524, 32523, 1338369, 8287, 117571, 117570, 7776, 7742, 89593, 7711,
            33511, 33213, 6072, 33208, 33154, 2759, 131567])

    @attr('taxid')
    def test_taxid_lineage_name(self):
        taxid = self._buildTaxaDBObject(TaxID)
        lineage = taxid.lineage_name(37081)
        self.assertListEqual(lineage, [
            'Spheniscus magellanicus', 'Spheniscus', 'Spheniscidae',
            'Sphenisciformes', 'Neognathae', 'Aves', 'Coelurosauria',
            'Theropoda', 'Saurischia', 'Dinosauria', 'Archosauria',
            'Archelosauria', 'Sauria', 'Sauropsida', 'Amniota', 'Tetrapoda',
            'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi', 'Teleostomi',
            'Gnathostomata', 'Vertebrata', 'Craniata', 'Chordata', 'Deuterostomia',
            'Bilateria', 'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota',
            'cellular organisms'])
