#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import os
import sys
from taxadb.schema import Taxa


class TaxaParser(object):
    """
    Main parser class for taxonomic files
    """

    def __init__(self):
        """
        Base class
        """
        pass

    def check_file(self, element):
        """
        Make some check on a file
        :param element: File to check
        :type element: str
        :return: True
        :rtype: bool
        :raise `SystemExit`: if input file does not exist
        :raise `SystemExit`: if input is not a file
        """
        if element is None:
            self.fatal("Please provide an input file to check")
        if not os.path.exists(element):
            self.fatal("File %s does not exist" % str(element))
        if not os.path.isfile(element):
            self.fatal("%s is not a file" % str(element))
        return True

    @classmethod
    def fatal(cls, msg):
        """

        :param msg: Error message to print
        :return:
        """
        if msg is not None:
            print("[FATAL] %s" % str(msg), file=sys.stderr)
        else:
            print("[FATAL] An error occured", file=sys.stderr)
        sys.exit(1)


class TaxaDumpParser(TaxaParser):
    """
    Main parser class for taxdump files
    """

    def __init__(self, nodes_files=None, names_file=None):
        """

        """
        super().__init__()
        self.nodes_file = nodes_files
        self.names_file = names_file

    def taxdump(self, nodes_file=None, names_file=None):
        """Parse the nodes.dmp and names.dmp files (from taxdump.tgz) and insert
        taxons in the Taxa table.

        Arguments:
        nodes_file -- the nodes.dmp file
        names_file -- the names.dmp file
        """
        if nodes_file is None:
            nodes_file = self.nodes_file
        if names_file is None:
            names_file = self.names_file
        self.check_file(names_file)
        self.check_file(nodes_file)
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
        for nodes, names in zip(nodes_data, names_data):
            taxa_info = {**nodes, **names}  # PEP 448, requires python 3.5
            taxa_info_list.append(taxa_info)
        print('merge successful')
        return taxa_info_list

    def set_nodes_files(self, nodes_file):
        """
        Set the accession file to use
        :param nodes_file: Nodes file to be set
        :type nodes_file: str
        :return: True
        :rtype: bool
        :raise `SystemExit`: If argument is None or not a file (`check_file`)
        """
        if nodes_file is None:
            self.fatal("Please provide an accession file to set")
        self.check_file(nodes_file)
        self.nodes_file = nodes_file
        return True

    def set_names_files(self, names_file):
        """
        Set the accession file to use
        :param names_file: Nodes file to be set
        :type names_file: str
        :return: True
        :rtype: bool
        :raise `SystemExit`: If argument is None or not a file (`check_file`)
        """
        if names_file is None:
            self.fatal("Please provide an accession file to set")
        self.check_file(names_file)
        self.names_file = names_file
        return True

    
class Accession2TaxidParser(TaxaParser):
    """

    """

    def __init__(self, acc_file=None, chunk=500):
        """

        :param chunk:
        """
        super().__init__()
        self.acc_file = acc_file
        self.chunk = chunk

    def accession2taxid(self, acc2taxid=None, chunk=500):
        """Parses the accession2taxid files and insert sequences in Sequences table(s).

        Arguments:
        acc2taxid -- input file (gzipped)
        chunk -- Chunk size of entries to gather before yielding, default 500
        """
        # Some accessions (e.g.: AAA22826) have a taxid = 0
        entries = []
        counter = 0
        taxids = {}
        if acc2taxid is None:
            acc2taxid = self.acc_file
        self.check_file(acc2taxid)
        if not chunk:
            chunk = self.chunk
        with gzip.open(acc2taxid, 'rb') as f:
            f.readline()  # discard the header
            for line in f:
                line_list = line.decode().rstrip('\n').split('\t')
                if not line_list[2] in taxids:
                    try:
                        Taxa.get(Taxa.ncbi_taxid == int(line_list[2]))
                        taxids[line_list[2]] = True
                    except Taxa.DoesNotExist:
                        taxids[line_list[2]] = False
                        continue
                if taxids[line_list[2]]:
                    data_dict = {
                        'accession': line_list[0],
                        'taxid': line_list[2]
                    }
                    entries.append(data_dict)
                    counter += 1
                if counter == chunk:
                    yield(entries)
                    entries = []
                    counter = 0
            if len(entries):
                yield(entries)

    def set_accession_file(self, acc_file):
        """
        Set the accession file to use
        :param acc_file: File to be set
        :type acc_file: str
        :return: True
        :rtype: bool
        :raise `SystemExit`: If argument is None or not a file (`check_file`)
        """
        if acc_file is None:
            self.fatal("Please provide an accession file to set")
        self.check_file(acc_file)
        self.acc_file = acc_file
        return True