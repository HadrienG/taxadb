from taxadb.schema import Taxa
from taxadb.taxadb import TaxaDB


class TaxID(TaxaDB):

    """Main class for querying taxid

    Provide methods to request taxa table and get associated accession ids.

    Args:
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname, config, dbtype, dbname)

    Raises:
        SystemExit: If table `taxa` does not exist

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        except Taxa.DoesNotExist:
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
        except Taxa.DoesNotExist:
            return None

    def lineage_name(self, taxid, reverse=False):
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
        except Taxa.DoesNotExist:
            return None
