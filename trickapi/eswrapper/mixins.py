from django.conf import settings
from .mapping_script import ES
from copy import deepcopy


def get_prefix():
    prefix = settings.ES_INDEX_PREFIX
    if settings.TESTING:
        prefix = "test_" + prefix
    return prefix


class ESWrapperMixin(object):

    '''ESWrapper Mixin for django models'''

    @classmethod
    def get_index_name(cls):
        '''Get the elasticsearch index name.'''
        return "{0}{1}_index".format(get_prefix(), cls.__name__.lower())

    @classmethod
    def get_document_type(cls):
        '''Get the elasticsearch document_type.'''
        return "{}_document".format(cls.__name__.lower())

    def get_document_body(self):
        '''
        Get the python dict that will represent the document body.
        By default will return a dictionary very similar to the value of `self.__dict__`.
        '''
        doc_dict = deepcopy(self.__dict__)
        doc_dict.pop('_state')
        return doc_dict


class ESTestMixin(object):

    '''Make sure any test indexes get removed from the elasticsearch node'''

    def tearDown(self):
        indices = ES.indices.get(index=['*'])
        test_indices = [name for name in indices.keys() if name.startswith('test_')]
        if test_indices:
            ES.indices.delete(index=test_indices)
