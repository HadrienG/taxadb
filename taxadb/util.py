#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import hashlib
import logging


def md5_check(file, block_size=256*128):
    """Check the md5 of files large or small

    Args:
        file (str): input file
        block_size (int): block_size for the file chunks. Default = 256*128
    """
    logger = logging.getLogger(__name__)

    logger.info('Checking md5 of %s' % file)
    md5 = open(file + '.md5').readline().split()[0]
    file_md5 = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            file_md5.update(chunk)
    try:
        assert(file_md5.hexdigest() == md5)
    except AssertionError as e:
        logger.error('Checking md5 of %s: NOT OK' % file)
        logger.error('Incomplete download of %s. Aborting' % file)
        sys.exit(1)
    else:
        logger.info('Checking md5 of %s: OK' % file)
