#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from taxa_db import *


def db_install_test():
    create_db()
    proc = subprocess.Popen(
        ['sqlite3', 'test.sqlite', '.tables'],
        stdout=subprocess.PIPE)
    db_call = proc.stdout.read()
    assert db_call == b'sequence  taxa    \n'
