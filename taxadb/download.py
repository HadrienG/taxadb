#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import logging
import tarfile
import requests

from tqdm import tqdm


def ncbi(path, filename, base_url='https://ftp.ncbi.nlm.nih.gov/'):
    """Download a file from the NCBI ftp using https

    Arguments:
        path (string): base path to the file
        filename (string): filename
        base_url (string): address to the ncbi ftp
    """
    logger = logging.getLogger(__name__)

    url = base_url + path + filename
    request = requests.get(url, stream=True)

    logger.info('Downloading %s' % filename)
    total_size = int(request.headers.get('content-length', 0))
    chunk_size = 1024
    written = 0
    with open(filename, 'wb') as f:
        for chunk in tqdm(request.iter_content(chunk_size=chunk_size),
                          total=total_size/chunk_size,
                          unit='Kb', unit_scale=True):
            if chunk:
                f.write(chunk)
                f.flush()


def unpack(filename):
    """uncompress a tar.gz archive
    """
    logger = logging.getLogger(__name__)

    logger.info('Unpacking %s' % filename)
    with tarfile.open(filename, "r:gz") as archive:
        archive.extractall()
        archive.close()
