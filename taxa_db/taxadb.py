#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

import os
import gzip
import tarfile
import ftputil
import hashlib
import argparse


def _md5_check(file, block_size=256*128):
    print('Checking md5')
    md5 = open(file + '.md5').readline().split()[0]
    file_md5 = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            file_md5.update(chunk)
    assert(file_md5.hexdigest() == md5)
    print('Done!!')


def download(args):
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


def create_db():
    db = SqliteDatabase('test.sqlite')
    db.connect()
    db.create_table(Taxa)
    db.create_table(Sequence)


def main():
    parser = argparse.ArgumentParser(prog='taxadb')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_download = subparsers.add_parser('download', help='download files')
    parser_download.add_argument(
        '--outdir',
        '-o',
        metavar='dir',
        help='Output Directory'
    )
    parser_download.set_defaults(func=download)

    parser_create = subparsers.add_parser('create', help='create database')
    parser_create.add_argument(
        '--dbname',
        '-d',
        default='taxadb'
        help='name of the database (default: %(default)s))'
    )
    parser_create.add_argument(
        '--dbtype',
        '-t',
        choices=['sqlite', 'mysql', 'postgres']
        default='sqlite'
        help='type of the database (default: %(default)s))'
    )

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(e)
        parser.print_help()

    # create_db()

if __name__ == '__main__':
    main()
