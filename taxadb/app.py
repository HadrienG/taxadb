#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

import os
import gzip
import tarfile
import ftputil
import hashlib
import argparse

from taxadb.schema import *


def _md5_check(file, block_size=256*128):
    """Check the md5 of large files

    Arguments:
    file -- input file
    block_size -- block_size for the file chunks. default = 256*128
    """
    print('Checking md5')
    md5 = open(file + '.md5').readline().split()[0]
    file_md5 = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            file_md5.update(chunk)
    assert(file_md5.hexdigest() == md5)
    print('Done!!')


def _parse_taxdump(nodes_file, names_file):
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
    # insert in database
    with db.atomic():
        for i in range(0, len(taxa_info_list), 500):
            Taxa.insert_many(taxa_info_list[i:i+500]).execute()
    print('Taxa: completed')


def _parse_accession2taxid(acc2taxid):
    """Parse the accession2taxid files. and insert
    squences in the Sequence table.

    Arguments:
    acc2taxid -- input file (gzipped)
    """
    with db.atomic():
        with gzip.open(acc2taxid, 'rb') as f:
            f.readline()  # discard the header
            for line in f:
                line_list = line.decode().rstrip('\n').split('\t')
                data_dict = {
                    'accession': line_list[0],
                    'taxid': line_list[2]
                }
                Sequence.create(**data_dict)
    print('%s added to database' % (acc2taxid))


def download(args):
    """Main function for the 'taxadb download' sub-command. This function
    downloads taxump.tar.gz and the content of the accession2taxid directory
    from the ncbi ftp.

    Arguments:
    args -- parser from the argparse library. contains:
    args.outdir -- output directory
    """
    ncbi_ftp = 'ftp.ncbi.nlm.nih.gov'

    # files to download in accession2taxid
    nucl_est = 'nucl_est.accession2taxid.gz'
    nucl_gb = 'nucl_gb.accession2taxid.gz'
    nucl_gss = 'nucl_gss.accession2taxid.gz'
    nucl_wgs = 'nucl_wgs.accession2taxid.gz'
    prot = 'prot.accession2taxid.gz'
    acc_dl_list = [nucl_est, nucl_gb, nucl_gss, nucl_wgs, prot]
    taxdump = 'taxdump.tar.gz'

    out = args.outdir
    os.makedirs(os.path.dirname(out), exist_ok=True)
    os.chdir(os.path.dirname(out))

    for file in acc_dl_list:
        print('Started Downloading %s' % (file))
        with ftputil.FTPHost(ncbi_ftp, 'anonymous', 'password') as ncbi:
            ncbi.chdir('pub/taxonomy/accession2taxid/')
            ncbi.download_if_newer(file, file)
            ncbi.download_if_newer(file + '.md5', file + '.md5')
            _md5_check(file)

    print('Started Downloading %s' % (taxdump))
    with ftputil.FTPHost(ncbi_ftp, 'anonymous', 'password') as ncbi:
        ncbi.chdir('pub/taxonomy/')
        ncbi.download_if_newer(taxdump, taxdump)
        ncbi.download_if_newer(taxdump + '.md5', taxdump + '.md5')
        _md5_check(taxdump)
    print('Unpacking %s' % (taxdump))
    with tarfile.open(taxdump, "r:gz") as tar:
        tar.extractall()
        tar.close()


def create_db(args):
    """Main function for the 'taxadb create' sub-command. This function
    creates a taxonomy database with 2 tables: Taxa and Sequence.

    Arguments:
    args -- parser from the argparse library. contains:
    args.input -- input directory. It is the directory created by
        'taxadb download'
    args.dbname -- name of the database to be created
    args.dbtype -- type of database to be used. Currently only sqlite is
        supported
    """
    if args.dbtype == 'sqlite':
        database = pw.SqliteDatabase('%s.sqlite' % (args.dbname))
    elif args.dbtype == 'mysql':
        if args.username is None or args.password is None:
            print('--dbtype mysql requires --username and --password.\n')
        database = pw.MySQLDatabase(
            args.dbname,
            user=args.username,
            password=args.password
            )
    db.initialize(database)

    db.connect()
    db.create_table(Taxa)
    db.create_table(Sequence)
    _parse_taxdump(args.input + '/nodes.dmp', args.input + '/names.dmp')
    _parse_accession2taxid(args.input + '/nucl_est.accession2taxid.gz')
    _parse_accession2taxid(args.input + '/nucl_gb.accession2taxid.gz')
    _parse_accession2taxid(args.input + '/nucl_gss.accession2taxid.gz')
    _parse_accession2taxid(args.input + '/nucl_wgs.accession2taxid.gz')
    _parse_accession2taxid(args.input + '/prot.accession2taxid.gz')
    db.close()


def main():
    parser = argparse.ArgumentParser(
        prog='taxadb',
        usage='taxadb <command> [options]',
        description='download and create the database used by the taxadb \
        library'
    )
    subparsers = parser.add_subparsers(
        title='available commands',
        metavar=''
    )

    parser_download = subparsers.add_parser(
        'download',
        prog='taxadb download',
        description='download the files required to create the database',
        help='download the files required to create the database'
    )
    parser_download.add_argument(
        '--outdir',
        '-o',
        metavar='<dir>',
        help='Output Directory',
        required=True
    )
    parser_download.set_defaults(func=download)

    parser_create = subparsers.add_parser(
        'create',
        prog='taxadb create',
        description='build the database',
        help='build the database'
    )
    parser_create.add_argument(
        '--input',
        '-i',
        metavar='<dir>',
        help='Input directory (where you first downloaded the files)',
        required=True
    )
    parser_create.add_argument(
        '--dbname',
        '-d',
        default='taxadb',
        metavar='taxadb',
        help='name of the database (default: %(default)s))'
    )
    parser_create.add_argument(
        '--dbtype',
        '-t',
        choices=['sqlite', 'mysql'],
        default='sqlite',
        metavar='[sqlite|mysql]',
        help='type of the database (default: %(default)s))'
    )
    parser_create.add_argument(
        '--username',
        '-u',
        help='Username to login as (required for MySQLdatabase)'
    )
    parser_create.add_argument(
        '--password',
        '-p',
        help='Password to use (required for MySQLdatabase)'
    )
    parser_create.set_defaults(func=create_db)

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        parser.print_help()
        print('\n%s' % e)  # for debugging purposes
