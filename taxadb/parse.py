#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip


def taxdump(nodes_file, names_file):
    """Parse the nodes.dmp and names.dmp files (from taxdump.tgz) and insert
    taxons in the Taxa table.

    Arguments:
    nodes_file -- the nodes.dmp file
    names_file -- the names.dmp file
    """
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
    taxa_info = {}
    for nodes, names in zip(nodes_data, names_data):
        taxa_info = {**nodes, **names}  # PEP 448, requires python 3.5
        taxa_info_list.append(taxa_info)
    print('merge successful')
    return taxa_info_list


def accession2taxid(acc2taxid):
    """Parse the accession2taxid files. and insert
    squences in the Sequence table.

    Arguments:
    acc2taxid -- input file (gzipped)
    """
    with gzip.open(acc2taxid, 'rb') as f:
        f.readline()  # discard the header
        for line in f:
            line_list = line.decode().rstrip('\n').split('\t')
            data_dict = {
                'accession': line_list[0],
                'taxid': line_list[2]
            }
            yield(data_dict)
