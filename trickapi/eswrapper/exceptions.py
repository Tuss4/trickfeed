INDEX_NOT_FOUND = "Index '{}' not found on node."
DOC_NOT_FOUND = "Document with id '{0}' not found on index '{1}'."


class IndexNotFound(Exception):

    """
    Exception to be raised when an index is not found.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(INDEX_NOT_FOUND.format(self.value))


class DocumentNotFound(Exception):

    """
    Exception to be raised when a Document is not found.
    """

    def __init__(self, index_name, doc_id):
        self.index_name = index_name
        self.document_id = doc_id

    def __str__(self):
        return repr(DOC_NOT_FOUND.format(self.document_id, self.index_name))
