from django.conf import settings

from importlib import import_module
from elasticsearch import Elasticsearch


ES = Elasticsearch([dict(host=settings.ES_URL)])

CHARFIELD = 'CharField'
AUTOFIELD = 'AutoField'
DATEFIELD = 'DateField'


def update_properties_dict(props, k, field_type):
    if not props.get(k):
        if k == 'id' and field_type == AUTOFIELD:
            props[k] = {"type": "long"}
        if field_type == CHARFIELD:
            props[k] = {"type": "string"}
        if field_type == DATEFIELD:
            props[k] = {"type": "string"}


def get_mapping_name(model):
    return '{}_MAPPING'.format(model.__name__.upper())


def create_mapping(app_config, model):
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
    f = open(path, 'w')
    f.write('{0} = {1}'.format(mapping_name, map_dict))
    f.close()


def create_index(app_config, model):
    m = app_config.get_model(model)
    module_name = '{}.es_mappings'.format(app_config.name)
    try:
        module = import_module(module_name)
        mappings = getattr(module, get_mapping_name(m))
        print mappings
        ES.indices.create(
            index=m.get_index_name(), body=mappings)
    except ImportError as e:
        print e
