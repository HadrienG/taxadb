#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import ftputil
import hashlib

# files to download in accession2taxid
NUCL_EST = 'nucl_est.accession2taxid.gz'
NUCL_GB = 'nucl_gb.accession2taxid.gz'
NUCL_GSS = 'nucl_gss.accession2taxid.gz'
NUCL_WGS = 'nucl_wgs.accession2taxid.gz'
PROT = 'prot.accession2taxid.gz'
ACC_DL_LIST = [NUCL_EST, NUCL_GB, NUCL_GSS, NUCL_WGS, PROT]

# taxdump
TAXDUMP = 'taxdump.tar.gz'


def md5_check(file):
    print('Checking md5')
    md5 = open(file + '.md5').readline().split()[0]
    file_md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
    assert(file_md5 == md5)
    print('Done!!')


def get_acc2taxid(ACC_DL_LIST):
    for file in ACC_DL_LIST:
        print('Started Downloading %s' % (file))
        ncbi = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')
        ncbi.chdir('pub/taxonomy/accession2taxid/')
        ncbi.download_if_newer(file, file)
        ncbi.download_if_newer(file + '.md5', file + '.md5')
        md5_check(file)


def get_taxdump(TAXDUMP):
    print('Started Downloading %s' % (TAXDUMP))
    ncbi = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')
    ncbi.chdir('pub/taxonomy/')
    ncbi.download_if_newer(TAXDUMP, TAXDUMP)
    ncbi.download_if_newer(TAXDUMP + '.md5', TAXDUMP + '.md5')
    md5_check(file)


def main():
    get_acc2taxid(ACC_DL_LIST)
    # TODO: the read() method is likely to fail on large file as it needs a
    # continuous block of memory. Nedd to find an alternative.
    # maybe http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    # print(hashlib.md5(open(NUCL_WGS, 'rb').read()).hexdigest())

if __name__ == '__main__':
    main()
