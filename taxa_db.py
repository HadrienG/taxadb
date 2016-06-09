#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *


def main():
    db = SqliteDatabase('test.sqlite')

    class Person(Model):
        name = CharField()
        birthday = DateField()
        is_relative = BooleanField()

        class Meta:
            database = db

    db.connect()
    db.create_table(Person)


if __name__ == '__main__':
    main()
