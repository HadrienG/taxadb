#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import tarfile
import ftputil
import hashlib

NCBI = 'ftp.ncbi.nlm.nih.gov'

# files to download in accession2taxid
NUCL_EST = 'nucl_est.accession2taxid.gz'
NUCL_GB = 'nucl_gb.accession2taxid.gz'
NUCL_GSS = 'nucl_gss.accession2taxid.gz'
NUCL_WGS = 'nucl_wgs.accession2taxid.gz'
PROT = 'prot.accession2taxid.gz'
ACC_DL_LIST = [NUCL_EST, NUCL_GB, NUCL_GSS, NUCL_WGS, PROT]

# taxdump
TAXDUMP = 'taxdump.tar.gz'


def md5_check(file, block_size=256*128):
    print('Checking md5')
    md5 = open(file + '.md5').readline().split()[0]
    file_md5 = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            file_md5.update(chunk)
    assert(file_md5.hexdigest() == md5)
    print('Done!!')


def get_acc2taxid(ACC_DL_LIST):
    for file in ACC_DL_LIST:
        print('Started Downloading %s' % (file))
        with ftputil.FTPHost(NCBI, 'anonymous', 'password') as ncbi:
            ncbi.chdir('pub/taxonomy/accession2taxid/')
            ncbi.download_if_newer(file, file)
            ncbi.download_if_newer(file + '.md5', file + '.md5')
            md5_check(file)


def get_taxdump(TAXDUMP):
    print('Started Downloading %s' % (TAXDUMP))
    with ftputil.FTPHost(NCBI, 'anonymous', 'password') as ncbi:
        ncbi.chdir('pub/taxonomy/')
        ncbi.download_if_newer(TAXDUMP, TAXDUMP)
        ncbi.download_if_newer(TAXDUMP + '.md5', TAXDUMP + '.md5')
        md5_check(TAXDUMP)
    print('Unpacking %s' % (TAXDUMP))
    with tarfile.open(TAXDUMP, "r:gz") as tar:
        tar.extractall()
        tar.close()


def main():
    get_acc2taxid(ACC_DL_LIST)
    get_taxdump(TAXDUMP)

if __name__ == '__main__':
    main()
