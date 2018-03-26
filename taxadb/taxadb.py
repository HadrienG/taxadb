import sys
import logging

from peewee import PeeweeException

from taxadb.schema import db, DatabaseFactory


class TaxaDB(object):

    """Main TaxaDB package class

    Parent class of the Taxadb application. Use this class to create inheriting
    classes.

    Args:
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname, config, dbtype, dbname)

    Raises:
        AttributeError: If cannot instantiate `taxadb.schema.DatabaseFactory`.
    Attributes:
        MAX_LIST (:obj:`int`): Maximum number of bind variables to pass to
            request methods. Due to SQLite limit of passed arguments to a
            statement, we limit number of accession and taxid to
            request to 999 (https://www.sqlite.org/c3ref/bind_blob.html)
    """

    MAX_LIST = 999

    @property
    def logger(self):
        component = "{}.{}".format(type(self).__module__, type(self).__name__)
        return logging.getLogger(component)

    def __init__(self, **kwargs):
        self.db = None
        try:
            self.dbfact = DatabaseFactory(**kwargs)
            self.database = self.dbfact.get_database()
            self.db = db
            self.db.initialize(self.database)
            self.db.connect()
        except (AttributeError, PeeweeException) as err:
            self.logger.error("Can't create database object: %s" % str(err))
            sys.exit(1)

    def __del__(self):
        """Ensure database connection is closed"""
        if self.db and self.db is not None and not self.db.is_closed():
            self.db.close()

    def check_table_exists(cls, table):
        """Check a table exists in the database

        Args:
            table (:obj:`str`): Database `table` name to check.

        Returns:
            True

        Raises:
             SystemExit: if `table` does not exist
        """
        logger = logging.getLogger('TaxaDB')
        if not table.table_exists():
            logger.error(
                "Table %s does not exist" % (str(table.get_table_name())))
            sys.exit(1)
        return True

    @staticmethod
    def check_list_ids(ids):
        """Check the list of ids is not longer that MAX_LIST

        Args:
            ids (:obj:`list`): List of bind values

        Returns:
            True

        Raises:
            SystemExit: If `len` of the list of greater than `MAX_LIST`.
        """
        logger = logging.getLogger('TaxaDB')
        if len(ids) > TaxaDB.MAX_LIST:
            logger.error(
                "Too many accession entries to request (%d), max %d"
                % (len(ids), TaxaDB.MAX_LIST))
            sys.exit(1)
        return True

    def get(self, name):
        """Get a database setting from the connection arguments

        Returns:
            value (:obj:`str`) if found, None otherwise
        """
        value = self.dbfact.get(name)
        return value

    def set(self, option, value, section=DatabaseFactory.DEFAULT_SECTION):
        """Set a configuration value

        Args:
            option (:obj:`str`): Config key
            value (:obj:`str`): Config value
            section (:obj:`str`): Config section, default 'DBSETTINGS'

        Returns:
            True
        """
        return self.dbfact.set(option, value, section=section)

    def _unmapped_taxid(self, acc, do_exit=False):
        """Prints error message to stderr if an accession number is not
        mapped with a taxid

        Source ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/README
        >> If for some reason the source organism cannot be mapped to the
        taxonomy database, the column will contain 0.<<

        Args:
            acc (:obj:`str`): Accession number not mapped with taxid
            do_exit (:obj:`bool`): Exit with code 1. Default False
        """
        self.logger.error(
            "No taxid mapped for accession %s" % str(acc))
        if do_exit:
            sys.exit(1)
        return True
