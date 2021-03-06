from .script import ES


class ESManager(object):

    '''
    Elasticsearch index and documents manager.
    Superficially similar to how models.Manager works.
    '''

    def __init__(self, model=None):
        if model:
            self.model = model

    def get_model(self):
        return self.model

    def index(self):
        return self.get_model().get_index_name()

    def doc_type(self):
        return self.get_model().get_document_type()

    def return_list(self, es_queryset):
        return [doc['_source'] for doc in es_queryset['hits']['hits']]

    def all(self):
        es_qs = ES.search(
            index=[self.index()],
            doc_type=[self.doc_type()],
            q='*',
            size=self.get_model().objects.count())
        return self.return_list(es_qs)

    def search(self, body, size=20):
        es_qs = ES.search(
            index=[self.index()],
            doc_type=[self.doc_type()],
            size=size,
            body=body
        )
        return self.return_list(es_qs)
