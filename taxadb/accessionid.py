from taxadb.schema import Accession, Taxa
from taxadb.taxadb import TaxaDB


class AccessionID(TaxaDB):

    """Main accession class

    Provide methods to request accession table and get associated taxonomy for
        accession ids.

    Args:
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname, config, dbtype, dbname)

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
        with self.db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                yield (i.accession, i.taxid.ncbi_taxid)
            # TODO: List accession ID not found?
            # for noid in notfound:
            #     self._unmapped_taxid(noid)

    def sci_name(self, acc_number_list):
        """Get taxonomic scientific name for accession ids

        Given a list of accession numbers, yield the accession number and their
        associated scientific name as tuples

        Args:
            acc_number_list (:obj:`list`): a list of accession numbers

        Yields:
            tuple: (accession id, taxonomy id)

        """
        self.check_list_ids(acc_number_list)
        with self.db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                yield (i.accession, i.taxid.tax_name)
            # TODO: List accession ID not found?
            # for noid in notfound:
            #     self._unmapped_taxid(noid)

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
        with self.db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
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
            # TODO: List accession ID not found?
            # for noid in notfound:
            #     self._unmapped_taxid(noid)

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
        with self.db.atomic():
            query = Accession.select().where(
                Accession.accession << acc_number_list)
            for i in query:
                lineage_list = []
                current_lineage = i.taxid.tax_name
                parent = i.taxid.parent_taxid
                while current_lineage != 'root':
                    lineage_list.append(current_lineage)
                    new_query = Taxa.get(Taxa.ncbi_taxid == parent)
                    current_lineage = new_query.tax_name
                    parent = new_query.parent_taxid
                yield (i.accession, lineage_list)
            # TODO: List accession ID not found?
            # for noid in notfound:
            #     self._unmapped_taxid(noid)
