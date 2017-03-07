from taxadb.schema import *
from taxadb.util import fatal
import sys


class TaxaDB(object):
    """Main TaxaDB package class

    Args:
        dbname (:obj:`str`): Database name to connect to
        dbtype (:obj:`str`): Database type to connect to (`sqlite`, `postgre`,
            `mysql`). Default `sqlite`
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname)

    Raises:
        AttributeError: If cannot instantiate `taxadb.schema.DatabaseFactory`.
    Attributes:
        MAX_LIST (:obj:`int`): Maximum number of bind variables to pass to
            request methods. Due to SQLite limit of passed arguments to a
            statement, we limit number of accession and taxid to
            request to 999 (https://www.sqlite.org/c3ref/bind_blob.html)
    """

    MAX_LIST = 999

    def __init__(self, dbname=None, dbtype='sqlite', **kwargs):
        self.db = None
        self.dbname = dbname
        try:
            self.database = DatabaseFactory(
                dbname=dbname,
                dbtype=dbtype,
                **kwargs).get_database()
        except AttributeError as err:
            fatal("Can't create database object: %s" % str(err))
        self.db = db
        self.db.initialize(self.database)
        self.db.connect()

    def __del__(self):
        """Ensure database connection is closed"""
        if self.db is not None and not self.db.is_closed():
            self.db.close()

    @classmethod
    def check_table_exists(cls, table):
        """Check a table exists in the database

        Args:
            table (:obj:`str`): Database `table` name to check.

        Returns:
            True

        Raises:
             SystemExit: if `table` does not exist
        """
        if not table.table_exists():
            fatal("Table %s does not exist" % (str(table._meta.db_table)))
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
        if len(ids) > TaxaDB.MAX_LIST:
            fatal("Too many accession entries to request (%d), max %d" % (
                        len(ids), AccessionID.MAX_LIST))
        return True

    def _unmapped_taxid(self, acc, do_exit=False):
        """Prints an error message on stderr an accession number is not mapped
            with a taxid

        Source ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/README
        >> If for some reason the source organism cannot be mapped to the
        taxonomy database, the column will contain 0.<<

        Args:
            acc (:obj:`str`): Accession number not mapped with taxid
            do_exit (:obj:`bool`): Exit with code 1. Default False
        """
        print("No taxid mapped for accession %s" % str(acc), file=sys.stderr)
        if do_exit:
            sys.exit(1)
        return True


class AccessionID(TaxaDB):
    """Main accession class

    Provide methods to request accession table and get associated taxonomy for
        accession ids.

    Args:
        dbtype (:obj:`str`): Database to connect to
        dbtype (:obj:`str`): Database type to connect to (`sqlite`, `postgre`,
            `mysql`). Default `sqlite`
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname)

    Raises:
        SystemExit: If table `accession` does not exist
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.check_table_exists(Accession)

    def taxid(self, acc_number_list):
        """Get taxonomy of accession ids

        Given a list of accession numbers, yield the accession number and their
        associated taxids as tuples

        Args:
            acc_number_list (:obj:`list`): a list of accession numbers

        Yields:
            tuple: (accession id, taxonomy id)

        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                try:
                    yield (i.accession, i.taxid.ncbi_taxid)
                except Taxa.DoesNotExist:
                    self._unmapped_taxid(i.accession)

    def sci_name(self, acc_number_list):
        """Get taxonomic scientific name for accession ids

        Given a list of acession numbers, yield the accession number and their
            associated scientific name as tuples

        Args:
            acc_number_list (:obj:`list`): a list of accession numbers

        Yields:
            tuple: (accession id, taxonomy id)

        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                try:
                    yield (i.accession, i.taxid.tax_name)
                except Taxa.DoesNotExist:
                    self._unmapped_taxid(i.accession)

    def lineage_id(self, acc_number_list):
        """Get taxonomic lineage name for accession ids

        Given a list of accession numbers, yield the accession number and their
            associated lineage (in the form of taxids) as tuples

        Args:
            acc_number_list (:obj:`list`): a list of accession numbers

        Yields:
            tuple: (accession id, lineage list)

        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                try:
                    lineage_list = []
                    current_lineage = i.taxid.tax_name
                    current_lineage_id = i.taxid.ncbi_taxid
                    parent = i.taxid.parent_taxid
                    while current_lineage != 'root':
                        lineage_list.append(current_lineage_id)
                        new_query = Taxa.get(Taxa.ncbi_taxid == parent)
                        current_lineage = new_query.tax_name
                        current_lineage_id = new_query.ncbi_taxid
                        parent = new_query.parent_taxid
                    yield (i.accession, lineage_list)
                except Taxa.DoesNotExist:
                    self._unmapped_taxid(i.accession)

    def lineage_name(self, acc_number_list):
        """Get a lineage name for accession ids

        Given a list of acession numbers, yield the accession number and their
            associated lineage as tuples

        Args:
            acc_number_list (:obj:`list`): a list of accession numbers

        Yields:
            tuple: (accession id, lineage name)

        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                try:
                    lineage_list = []
                    current_lineage = i.taxid.tax_name
                    parent = i.taxid.parent_taxid
                    while current_lineage != 'root':
                        lineage_list.append(current_lineage)
                        new_query = Taxa.get(Taxa.ncbi_taxid == parent)
                        current_lineage = new_query.tax_name
                        parent = new_query.parent_taxid
                    yield (i.accession, lineage_list)
                except Taxa.DoesNotExist:
                    self._unmapped_taxid(i.accession)


class TaxID(TaxaDB):
    """Main class for querying taxid

    Provide methods to request taxa table and get associated accession ids.

    Args:
        dbtype (:obj:`str`): Database to connect to
        dbtype (:obj:`str`): Database type to connect to (`sqlite`, `postgre`,
            `mysql`). Default `sqlite`
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname)

    Raises:
        SystemExit: If table `taxa` does not exist

    """

    def __init__(self, dbtype='sqlite', dbname=None, **kwargs):
        super().__init__(dbtype=dbtype, dbname=dbname, **kwargs)
        self.check_table_exists(Taxa)

    def sci_name(self, taxid):
        """Get taxonomic scientific name for taxonomy id

        Given a taxid, return its associated scientific name

        Args:
            taxid (:obj:`int`): a taxid
        Returns:
            str: name, scientific name or None if taxid not found

        """
        try:
            name = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
            return name
        except Taxa.DoesNotExist as err:
            return None

    def lineage_id(self, taxid, reverse=False):
        """Get lineage for a taxonomic id

        Given a taxid, return its associated lineage (in the form of a list of
            taxids, each parents of each others)

        Args:
            taxid (:obj:`int`): a taxid
            reverse (:obj:`bool`): Inverted lineage, from top to bottom
                taxonomy hierarchy. Default False
        Returns:
            list: lineage_list, associated lineage id with taxid or None if
                taxid not found

        """
        try:
            lineage_list = []
            current_lineage = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
            current_lineage_id = Taxa.get(Taxa.ncbi_taxid == taxid).ncbi_taxid
            parent = Taxa.get(Taxa.ncbi_taxid == taxid).parent_taxid
            while current_lineage != 'root':
                lineage_list.append(current_lineage_id)
                new_query = Taxa.get(Taxa.ncbi_taxid == parent)

                current_lineage = new_query.tax_name
                current_lineage_id = new_query.ncbi_taxid
                parent = new_query.parent_taxid
            if reverse is True:
                lineage_list.reverse()
            return lineage_list
        except Taxa.DoesNotExist as err:
            return None

    def lineage_name(slef, taxid, reverse=False):
        """Get a lineage name for a taxonomic id

        Given a taxid, return its associated lineage

        Arguments:
            taxid (:obj:`int`): a taxid
            reverse (:obj:`bool`): Inverted lineage, from top to bottom
                taxonomy hierarchy. Default False

        Returns:
            list: lineage_name, associated lineage name with taxid or None if
                taxid not found

        """
        try:
            lineage_list = []
            current_lineage = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
            parent = Taxa.get(Taxa.ncbi_taxid == taxid).parent_taxid
            while current_lineage != 'root':
                lineage_list.append(current_lineage)
                new_query = Taxa.get(Taxa.ncbi_taxid == parent)

                current_lineage = new_query.tax_name
                parent = new_query.parent_taxid
            if reverse is True:
                lineage_list.reverse()
            return lineage_list
        except Taxa.DoesNotExist as err:
            return None
