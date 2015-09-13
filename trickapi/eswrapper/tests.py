from django.test import TestCase
from .mixins import get_prefix
from videos.models import Video


class ESWrapperTests(TestCase):

    def test_get_prefix(self):
        prefix = get_prefix()
        self.assertTrue(prefix.startswith('test_'))

    def test_get_index_name(self):
        self.assertEqual(
            Video.get_index_name(), 'test_trickapi_video_index')
