from django.test import TestCase
from .mixins import get_prefix


class ESWrapperTests(TestCase):

    def test_get_prefix(self):
        prefix = get_prefix()
        self.assertTrue(prefix.startswith('test_'))
