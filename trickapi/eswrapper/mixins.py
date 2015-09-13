from django.conf import settings


def get_prefix():
    prefix = settings.ES_INDEX_PREFIX
    if settings.TESTING:
        prefix = "test_" + prefix
    return prefix


class ESWrapperMixin(object):

    @classmethod
    def get_index_name(cls):
        return "{0}{1}_index".format(get_prefix(), cls.__name__.lower())
