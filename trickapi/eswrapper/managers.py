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

    def all(self):
        return ES.search(
            index=[self.get_model().get_index_name()],
            doc_type=[self.get_model().get_document_type()],
            q='*',
            size=self.get_model().objects.count())['hits']['hits']

    # TODO: Finish this function
    def search(self, body):
        return "Lerhg"
