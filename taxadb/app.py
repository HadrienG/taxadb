#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tarfile
import ftputil
import argparse

from taxadb import util
from taxadb.parser import TaxaDumpParser, Accession2TaxidParser
from taxadb.schema import *


def download(args):
    """Main function for the 'taxadb download' sub-command.

    This function downloads taxump.tar.gz and the content of the accession2taxid
    directory from the ncbi ftp.

    Arguments:
             args.output (str): output directory

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
    """Main function for the 'taxadb create' sub-command.

    This function creates a taxonomy database with 2 tables: Taxa and Sequence.

    Args:

        args.input (str): input directory. It is the directory created by
            `taxadb download`
        args.dbname (str): name of the database to be created
        args.dbtype (str): type of database to be used.
        args.division (str): division to create the db for.

    """
    database = DatabaseFactory(**args.__dict__).get_database()
    div = args.division  # am lazy at typing
    db.initialize(database)

    nucl_est = 'nucl_est.accession2taxid.gz'
    nucl_gb = 'nucl_gb.accession2taxid.gz'
    nucl_gss = 'nucl_gss.accession2taxid.gz'
    nucl_wgs = 'nucl_wgs.accession2taxid.gz'
    prot = 'prot.accession2taxid.gz'
    acc_dl_list = []

    db.connect()
    parser = TaxaDumpParser(nodes_file=os.path.join(args.input, 'nodes.dmp'),
                            names_file=os.path.join(args.input, 'names.dmp'),
                            verbose=args.verbose)

    parser.verbose("Connected to database ...")
    # If taxa table already exists, do not recreate and fill it
    # safe=True prevent not to create the table if it already exists
    if not Taxa.table_exists():
        parser.verbose("Creating table %s" % str(Taxa._meta.db_table))
    db.create_table(Taxa, safe=True)
    parser = TaxaDumpParser(nodes_file=os.path.join(args.input, 'nodes.dmp'),
                            names_file=os.path.join(args.input, 'names.dmp'))
    parser.verbose("Parsing files")
    taxa_info_list = parser.taxdump()

    parser.verbose("Inserting taxa data")
    with db.atomic():
        for i in range(0, len(taxa_info_list), args.chunk):
            Taxa.insert_many(taxa_info_list[i:i+args.chunk]).execute()
    print('Taxa: completed')

    parser.verbose("Checking table accession ...")
    # At first load, table accession does not exist yet, we create it
    db.create_table(Accession, safe=True)

    if div in ['full', 'nucl', 'est']:
        acc_dl_list.append(nucl_est)
    if div in ['full', 'nucl', 'gb']:
        acc_dl_list.append(nucl_gb)
    if div in ['full', 'nucl', 'gss']:
        acc_dl_list.append(nucl_gss)
    if div in ['full', 'nucl', 'wgs']:
        acc_dl_list.append(nucl_wgs)
    if div in ['full', 'prot']:
        acc_dl_list.append(prot)
    parser = Accession2TaxidParser(verbose=args.verbose)
    with db.atomic():
        for acc_file in acc_dl_list:
            inserted_rows = 0
            parser.verbose("Parsing %s" % str(acc_file))
            for data_dict in parser.accession2taxid(acc2taxid=os.path.join(
                    args.input, acc_file), chunk=args.chunk):
                Accession.insert_many(data_dict[0:args.chunk]).execute()
                inserted_rows += len(data_dict)
            print('%s: %s added to database (%d rows inserted)' % (
                Accession._meta.db_table, acc_file, inserted_rows))
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
    parser.add_argument(
        '-v',
        '--verbose',
        action="store_true",
        default=False,
        dest="verbose",
        help="Prints verbose messages")

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
        '--chunk',
        '-c',
        metavar='<#chunk>',
        type=int,
        help='Number of sequences to insert in bulk (default: %(default)s)',
        default=500
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
        choices=['sqlite', 'mysql', 'postgres'],
        default='sqlite',
        metavar='[sqlite|mysql|postgres]',
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
        '--hostname',
        '-H',
        default='localhost',
        action="store",
        help='Database connection host (Optional, for MySQLdatabase and \
            PostgreSQLdatabase) (default: %(default)s)'
    )
    parser_create.add_argument(
        '--password',
        '-p',
        default=None,
        help='Password to use (required for MySQLdatabase \
            and PostgreSQLdatabase)'
    )
    parser_create.add_argument(
        '--port',
        '-P',
        help='Database connection port (default: 5432 (postgres), \
            3306 (MySQL))'
    )
    parser_create.add_argument(
        '--username',
        '-u',
        default=None,
        help='Username to login as (required for MySQLdatabase \
            and PostgreSQLdatabase)'
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
        print('\nERROR: %s' % str(e))  # for debugging purposes
