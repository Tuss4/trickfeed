from django.apps import apps
from django.test import TestCase

from .mixins import get_prefix, ESTestMixin
from .mapping_script import (
    create_index, ES, get_mapping_name, index_exists)
from videos.models import Video


class ESWrapperTests(ESTestMixin, TestCase):

    def test_get_prefix(self):
        prefix = get_prefix()
        self.assertTrue(prefix.startswith('test_'))

    def test_get_index_name(self):
        self.assertEqual(
            Video.get_index_name(), 'test_trickapi_video_index')

    def test_create_index(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(ES.indices.exists(index=[Video.get_index_name()]))

    def test_get_mapping_name(self):
        mapping_name = get_mapping_name(Video)
        self.assertEqual(mapping_name, "VIDEO_MAPPING")

    def test_index_exists(self):
        pass
