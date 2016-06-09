#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import ftputil
import hashlib


file = 'nucl_est.accession2taxid.gz'

ncbi = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')


def md5_check(file, md5):
    file_md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
    assert(file_md5 == md5)
    print('Yay!')


def get_acc2taxid(file):
    print('Started Downloading nucl_est.accession2taxid.gz')
    ncbi.chdir('pub/taxonomy/accession2taxid/')
    ncbi.download_if_newer(file, file)
    print('Done!')

    md5 = 'cb6c6cb691e48e26c3466aecb9b33d84'
    md5_check(file, md5)


def main():
    get_acc2taxid(file)

if __name__ == '__main__':
    main()
