from django.conf import settings

from importlib import import_module
from elasticsearch import Elasticsearch, NotFoundError
from .exceptions import IndexNotFound, DocumentNotFound


ES = Elasticsearch([dict(host=settings.ES_URL)])

CHARFIELD = 'CharField'
AUTOFIELD = 'AutoField'
DATEFIELD = 'DateField'
DATETIMEFIELD = 'DateTimeField'


def update_properties_dict(props, k, field_type):
    if not props.get(k):
        if k == 'id' and field_type == AUTOFIELD:
            props[k] = {"type": "long"}
        if field_type == CHARFIELD:
            props[k] = {"type": "string"}
        if field_type == DATEFIELD:
            props[k] = {"type": "date"}


def get_mapping_name(model):
    return '{}_MAPPING'.format(model.__name__.upper())


def create_mapping(app_config, model):
    # TODO: Check to see if variable is already in module
    m = app_config.get_model(model)
    fields = m._meta.get_fields()
    mapping_name = '{}_MAPPING'.format(m.__name__.upper())

    map_dict = {
        "mappings": {
            m.get_document_type(): {
                "properties": {}
            }
        }
    }

    for field in fields:
        props = map_dict['mappings'][m.get_document_type()]['properties']
        update_properties_dict(props, field.name, field.get_internal_type())

    path = app_config.path + '/es_mappings.py'
    f = open(path, 'a')
    f.write('{0} = {1}\n'.format(mapping_name, map_dict))
    f.close()


def create_index(app_config, model):
    m = app_config.get_model(model)
    module_name = '{}.es_mappings'.format(app_config.name)
    i_name = m.get_index_name()
    try:
        module = import_module(module_name)
        mappings = getattr(module, get_mapping_name(m))
        if not index_exists([i_name]):
            ES.indices.create(index=i_name, body=mappings)
        else:
            print "Index '{}' already exists.".format(i_name)
    except ImportError as e:
        print e


def index_exists(index_name):
    """
    Returns a boolean, based on the index's existence.
    """
    return ES.indices.exists(index=index_name)


def get_index(index_name):
    """Returns the index in a python dict."""
    try:
        return ES.indices.get(index=[index_name])
    except NotFoundError:
        raise IndexNotFound(index_name)


def delete_index(index_name):
    """
    Pass in an index_name to be deleted.
    Raises an IndexNotFound exception if the index is missing on the node.
    """
    try:
        ES.indices.delete(index=[index_name])
    except NotFoundError:
        raise IndexNotFound(index_name)


def create_document(obj):
    """
    Create a document based on instance of a model.
    Returns None if successful and an error string if it's not.
    """
    index = obj.get_index_name()
    doc_type = obj.get_document_type()
    body = obj.get_document_body()
    exists = ES.exists(index=index, doc_type=doc_type, id=obj.pk)

    if not exists:
        ES.create(index=index, doc_type=doc_type, body=body, id=obj.pk)
        return None

    return "Conflict: document already exists for {0} with id {1}.".format(
        obj.__class__.__name__, obj.pk)


def get_document(obj):
    """
    Get a document based on the instance.
    Raises a DocumentNotFound exception if the document is not found on the index.
    """
    try:
        return ES.get(
            index=obj.get_index_name(), doc_type=obj.get_document_type(), id=obj.pk)
    except NotFoundError:
        raise DocumentNotFound(obj.get_index_name(), obj.pk)


def update_document(obj):
    """
    Updates the document from the index.
    This should be called via a signal whenever the obj gets saved.
    """
    index = obj.get_index_name()
    doc_type = obj.get_document_type()
    body = dict(doc=obj.get_document_body())
    try:
        ES.update(index=index, doc_type=doc_type, body=body, id=obj.pk)
    except NotFoundError:
        raise DocumentNotFound(obj.get_index_name(), obj.pk)


def delete_document(obj):
    """
    Delete a document from the index.
    This should be called via a signal when the obj gets deleted.
    """
    index = obj.get_index_name()
    doc_type = obj.get_document_type()
    try:
        ES.delete(index=index, doc_type=doc_type, id=obj.pk)
    except NotFoundError:
        raise DocumentNotFound(obj.get_index_name(), obj.pk)
