#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import peewee as pw

from configparser import ConfigParser, NoSectionError


db = pw.Proxy()


class BaseModel(pw.Model):
    class Meta:
        database = db

    @classmethod
    def get_table_name(cls):
        """Get table name

        Returns:
            name (:obj:`str`): Table name in database
        """
        return cls._meta.table_name

    @classmethod
    def has_index(cls, name=None, columns=None):
        """Check if the table has an index (other than primary key)

        Search either by index name or by column name

        Args:
            name (:obj:`str`): Index name to check
            columns (:obj:`list`): List of columns making the index

        Returns:
            True or False

        Raises:
            SystemExit: If `table` object does not exists
        """
        if not cls.table_exists():
            return False
        # Returned object by get_indexes (namedtuple):
        # 'IndexMetadata', ('name', 'sql', 'columns', 'unique', 'table'))
        if name is not None:
            return cls._has_named_index(name)
        if columns is not None:
            return cls._has_columns_index(columns)
        return False

    @classmethod
    def _has_named_index(cls, name):
        indexes = db.get_indexes(cls.get_table_name())
        for idx in indexes:
            if idx[0] == name:
                return True
        return False

    @classmethod
    def _has_columns_index(cls, columns):
        if type(columns) is not list:
            return False
        indexes = db.get_indexes(cls.get_table_name())
        for idx in indexes:
            if sorted(columns) == sorted(idx[2]):
                return True
        return False


class Taxa(BaseModel):

    """table Taxa.

    Each row is a taxon.

    Attributes:
        ncbi_taxid (:obj:`pw.IntegerField`): the TaxID of
            the taxon (from nodes.dmp)
        parent_taxid (:obj:`pw.IntegerField`): the TaxID of
            the parent taxon (from nodes.dmp)
        tax_name (:obj:`pw.CharField`): the scientific name of
            the taxon (from names.dmp)
        lineage_level (:obj:`pw.CharField`): the level of lineage of
            the taxon (from nodes.dmp)

    """

    ncbi_taxid = pw.IntegerField(null=False, primary_key=True, unique=True)
    parent_taxid = pw.IntegerField(null=False)
    tax_name = pw.CharField()
    lineage_level = pw.CharField()


class Accession(BaseModel):

    """table Accession.

    Each row is a sequence from nucl_*.accession2taxid.gz. Each sequence
        has a taxid.

    Attributes:
        id (:obj:`pw.PrimaryKeyField`): the primary key
        taxid (:obj:`pw.ForeignKeyField`): reference to a taxon in the table
            Taxa.
        accession (:obj:`pw.CharField`): the accession number of the sequence.

    """

    id = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='accession')
    accession = pw.CharField(null=False, unique=True)


class DatabaseFactory(object):

    """Database factory to support multiple database type.

    This class may be used to create a database for different type (SQLite,
        PostgreSQL, MySQL).

    Args:
        config (:obj:`str`): Path to configuration file.
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname)
    Raises:
        AttributeError: If error occurred during database object build

    """

    SUPPORTED_DBS = ['sqlite', 'postgres', 'mysql']
    DEFAULT_SECTION = 'DBSETTINGS'

    def __init__(self, config=None, **kwargs):

        self.config = None
        self.set_config(config=config, args=kwargs)
        if not self.config.has_section(DatabaseFactory.DEFAULT_SECTION):
            raise AttributeError("No section %s defined in config"
                                 % DatabaseFactory.DEFAULT_SECTION)
        if self.get('dbtype') is None or self.get('dbtype') not in \
                DatabaseFactory.SUPPORTED_DBS:
            raise AttributeError(
                "Database type '%s' not supported" % str(self.get('dbtype')))
        if self.get('dbname') is None:
            raise AttributeError("A database name is required")
        self.args = kwargs

    def get_database(self):
        """Returns the correct database driver

        Returns:
            :obj:`pw.Database`
        Raises:
            AttributeError: if `--username` or `--password` not passed
                (if `--dbtype [postgres|mysql]`)

        """
        if self.get('dbtype') == 'sqlite':
            return pw.SqliteDatabase(self.get('dbname'),
                                     pragmas={'journal_mode': 'wal',
                                              'cache_size': -1 * 64000})
        else:
            if self.get('username') is None or self.get('password') is None:
                raise AttributeError('[ERROR] dbtype %s requires username and'
                                     ' password.\n' % str(self.get('dbtype')))
            if self.get('hostname') is None:
                self.set('hostname', 'localhost')
            if self.get('dbtype') == 'mysql':
                if self.get('port') is None or self.get('port') == '':
                    self.set('port', str(3306))
                return pw.MySQLDatabase(
                    self.get('dbname'),
                    user=self.get('username'),
                    password=self.get('password'),
                    host=self.get('hostname'),
                    port=int(self.get('port')))
            elif self.get('dbtype') == 'postgres':
                if self.get('port') is None or self.get('port') == '':
                    self.set('port', str(5432))
                return pw.PostgresqlDatabase(
                    self.get('dbname'),
                    user=self.get('username'),
                    password=self.get('password'),
                    host=self.get('hostname'),
                    port=int(self.get('port')))

    def get(self, name, section=DEFAULT_SECTION):
        """Get a database connection setting

        First checks if the configuration has been set and if the setting is
        in here. Otherwise, check if this setting is set as an attribute.

        Args:
            name (:obj:`str`): Database setting to request
            section (:obj:`str`): Section to look for, default 'DBSETTINGS'
        Returns:
            value (:obj:`str`) if set, None otherwise
        """
        if self.config is not None:
            if self.config.has_option(section, name):
                value = self.config.get(section, name, fallback=None)
                # When calling config.set, option and values must be string
                # so None is converted into 'None'
                if value == 'None':
                    return None
                return value
        return None

    def set(self, option, value, section=DEFAULT_SECTION):
        """Set a configuration value

        Args:
            option (:obj:`str`): Config key
            value (:obj:`str`): Config value
            section (:obj:`str`): Config section, default 'DBSETTINGS'

        Returns:
            True
        """
        if self.config is not None:
            try:
                self.config.set(section, str(option), str(value))
            except NoSectionError as err:
                raise AttributeError(str(err))
        return True

    def set_config(self, config=None, args=None):
        """Read configuration file with database settings

        It
        Args:
            config (:obj:`str`): Path to configuration file
            args (:obj:`dict`): Option arguments
        Returns:
            :obj:`configparser.ConfigParser`
        """
        # First we load configuration file if exists, from config
        # or from environment variable TAXADB_CONFIG
        self._load_config(config=config)
        # Then overwrite value from args passed from command line
        self._set_args(args=args)

    def _load_config(self, config=None):
        """Load configuration file

        Args:
            config (:obj:`str`): Path to configuration file

        Returns:
            True
        """
        config_file = config
        if config_file is None:
            env_file = os.environ.get('TAXADB_CONFIG')
            if env_file is not None and os.path.exists(env_file):
                config_file = env_file
        if config_file is not None:
            cfg = ConfigParser()
            config_file = os.path.abspath(config_file)
            cfg.read([config_file])
            self.config = cfg
        return True

    def _set_args(self, args):
        """Set database connection settings and info as config

        Args:
            args (:obj:`dict`): Dictionary for database settings
        Returns:
            True
        """
        if len(args.items()) != 0:
            if self.config is None:
                self.config = ConfigParser()
            if not self.config.has_section(DatabaseFactory.DEFAULT_SECTION):
                self.config.add_section(DatabaseFactory.DEFAULT_SECTION)
            for arg in args.items():
                self.set(arg[0], arg[1],
                         section=DatabaseFactory.DEFAULT_SECTION)
        return True
