from taxadb.schema import *
from taxadb.util import fatal


class TaxaDB(object):
    """
    Main TaxaDB package class
    """

    # Due to SQLite limit of passed arguments to a statement, we limit number of accession and taxid to
    # request to 999 (https://www.sqlite.org/c3ref/bind_blob.html)
    MAX_LIST = 999

    def __init__(self, dbname=None, dbtype='sqlite', **kwargs):
        """

        """
        self.db = None
        self.dbname = dbname
        try:
            self.database = DatabaseFactory(dbname=dbname, dbtype=dbtype, **kwargs).get_database()
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

        Arguments:
        table -- table name
        Throws `SystemExit` if table does not exist
        """
        if not table.table_exists():
            fatal("Table %s does not exist" % (str(table._meta.db_table)))
        return True

    @staticmethod
    def check_list_ids(ids):
        """Check the list of ids is not longer that MAX_LIST"""
        if len(ids) > TaxaDB.MAX_LIST:
            fatal("Too many accession entries to request (%d), max %d" % (len(ids), AccessionID.MAX_LIST))
        return True

    def _unmapped_taxid(self, acc, do_exit=False):
        """Prints an error message on stderr an accession number is not mapped with a taxid

        Source ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/README
        >> If for some reason the source organism cannot be mapped to the taxonomy
        database,
        the column will contain 0.<<

        Arguments:
        acc -- Accession number not mapped with taxid
        do_exit -- Exit with code 1, default False
        """
        print("No taxid mapped for accession %s" % str(acc), file=sys.stderr)
        if do_exit:
            sys.exit(1)
        return True


class AccessionID(TaxaDB):
    """
    Main accession class
    """

    def __init__(self, dbtype='sqlite', dbname=None, **kwargs):
        super().__init__(dbtype=dbtype, dbname=dbname, **kwargs)
        self.check_table_exists(Accession)

    def taxid(self, acc_number_list):
        """given a list of accession numbers, yield
        the accession number and their associated taxids as tuples

        Arguments:
        acc_number_list -- a list of accession numbers
        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(Accession.accession << acc_number_list)
            for i in query:
                try:
                    yield (i.accession, i.taxid.ncbi_taxid)
                except Taxa.DoesNotExist:
                    self._unmapped_taxid(i.accession)

    def sci_name(self, acc_number_list):
        """given a list of acession numbers, yield
        the accession number and their associated scientific name as tuples

        Arguments:
        acc_number_list -- a list of accession numbers
        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(Accession.accession << acc_number_list)
            for i in query:
                try:
                    yield (i.accession, i.taxid.tax_name)
                except Taxa.DoesNotExist:
                    self._unmapped_taxid(i.accession)

    def lineage_id(self, acc_number_list):
        """given a list of acession numbers, yield the accession number and their
        associated lineage (in the form of taxids) as tuples

        Arguments:
        acc_number_list -- a list of accession numbers
        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(Accession.accession << acc_number_list)
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
        """given a list of acession numbers, yield the accession number and their
        associated lineage as tuples

        Arguments:
        acc_number_list -- a list of accession numbers
        """
        self.check_list_ids(acc_number_list)
        with db.atomic():
            query = Accession.select().where(Accession.accession << acc_number_list)
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
    """Main class for querying taxid"""

    def __init__(self, dbtype='sqlite', dbname=None, **kwargs):
        super().__init__(dbtype=dbtype, dbname=dbname, **kwargs)
        self.check_table_exists(Taxa)

    def sci_name(self, taxid):
        """given a taxid, return its associated scientific name

        You can access data from several database type (sqlite3/mysql/postgresql)
        Arguments:
        taxid -- a taxid (int)
        Returns:
        name -- scientific name (str) or None if taxid not found
        """
        try:
            name = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
            return name
        except Taxa.DoesNotExist as err:
            return None

    def lineage_id(self, taxid, reverse=False):
        """given a taxid, return its associated lineage (in the form of a list
        of taxids, each parents of each others)

        Arguments:
        taxid -- a taxid (int)
        reverse -- Inverted lineage, from top to bottom taxonomy hierarchy
        Returns:
        lineage_list -- associated lineage id with taxid (list) or None if taxid not found
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
        """given a taxid, return its associated lineage

        Arguments:
        taxid -- a taxid (int)
        reverse -- Inverted lineage, from top to bottom taxonomy hierarchy
        Returns:
        lineage_name -- associated lineage name with taxid (list) or None if taxid not found
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
