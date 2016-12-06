#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

import os
import gzip
import tarfile
import ftputil
import argparse

from taxadb import util
from taxadb import parse

from taxadb import accession
from taxadb import taxid

from taxadb.schema import *


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
    os.makedirs(os.path.abspath(out), exist_ok=True)
    os.chdir(os.path.abspath(out))

    for file in acc_dl_list:
        print('Started Downloading %s' % (file))
        with ftputil.FTPHost(ncbi_ftp, 'anonymous', 'password') as ncbi:
            ncbi.chdir('pub/taxonomy/accession2taxid/')
            ncbi.download_if_newer(file, file)
            ncbi.download_if_newer(file + '.md5', file + '.md5')
            util.md5_check(file)

    print('Started Downloading %s' % (taxdump))
    with ftputil.FTPHost(ncbi_ftp, 'anonymous', 'password') as ncbi:
        ncbi.chdir('pub/taxonomy/')
        ncbi.download_if_newer(taxdump, taxdump)
        ncbi.download_if_newer(taxdump + '.md5', taxdump + '.md5')
        util.md5_check(taxdump)
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
    args.division -- division to create the db for. Full will build all the
        tables, prot will only build the prot table, nucl will build gb, wgs,
        gss and est
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
    div = args.division  # am lazy at typing
    db.initialize(database)

    nucl_est = 'nucl_est.accession2taxid.gz'
    nucl_gb = 'nucl_gb.accession2taxid.gz'
    nucl_gss = 'nucl_gss.accession2taxid.gz'
    nucl_wgs = 'nucl_wgs.accession2taxid.gz'
    prot = 'prot.accession2taxid.gz'
    acc_dl_dict = {}

    db.connect()
    db.create_table(Taxa)
    if div in ['full', 'nucl', 'est']:
        db.create_table(Est)
        acc_dl_dict[Est] = nucl_est
    if div in ['full', 'nucl', 'gb']:
        db.create_table(Gb)
        acc_dl_dict[Gb] = nucl_gb
    if div in ['full', 'nucl', 'gss']:
        db.create_table(Gss)
        acc_dl_dict[Gss] = nucl_gss
    if div in ['full', 'nucl', 'wgs']:
        db.create_table(Wgs)
        acc_dl_dict[Wgs] = nucl_wgs
    if div in ['full', 'prot']:
        db.create_table(Prot)
        acc_dl_dict[Prot] = prot
    taxa_info_list = parse.taxdump(
        args.input + '/nodes.dmp',
        args.input + '/names.dmp'
    )
    # insert in database
    with db.atomic():
        for i in range(0, len(taxa_info_list), 500):
            Taxa.insert_many(taxa_info_list[i:i+500]).execute()
    print('Taxa: completed')

    with db.atomic():
        for table, acc_file in acc_dl_dict.items():
            for data_dict in parse.accession2taxid(
                    args.input + '/' + acc_file):
                table.create(**data_dict)
            print('%s: %s added to database' % (table, acc_file))
    print('Sequence: completed')
    db.close()


def query(args):
    print('This has not been implemented yet. Sorry :-(')


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
        '-n',
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
        '--division',
        '-d',
        choices=['full', 'nucl', 'prot', 'gb', 'wgs', 'gss', 'est'],
        default='full',
        metavar='[full|nucl|prot|gb|wgs|gss|est]',
        help='division to build (default: %(default)s))'
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

    parser_query = subparsers.add_parser(
        'query',
        prog='taxadb query',
        description='query the database',
        help='query the database'
    )
    parser_query.set_defaults(func=query)

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        parser.print_help()
        print('\n%s' % e)  # for debugging purposes
