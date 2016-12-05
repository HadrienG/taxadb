#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def md5_check(file, block_size=256*128):
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
