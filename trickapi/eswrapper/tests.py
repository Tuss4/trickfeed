from django.apps import apps
from django.test import TestCase

import time

from .mixins import get_prefix, ESTestMixin
from .script import (
    create_index, ES, get_mapping_name, index_exists, get_index, delete_index,
    create_document, get_document, update_document, delete_document)
from .exceptions import IndexNotFound, DocumentNotFound
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
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))

    def test_get_index(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        index = get_index(Video.get_index_name())
        self.assertTrue(isinstance(index, dict))

    def test_delete_index(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        delete_index(Video.get_index_name())
        with self.assertRaises(IndexNotFound):
            get_index(Video.get_index_name())

    def test_create_document(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")
        err = create_document(v)
        self.assertIsNone(err)

    def test_create_document_conflict(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")
        err = create_document(v)
        self.assertIsNone(err)
        err = create_document(v)
        err_msg = "Conflict: document already exists for {0} with id {1}."
        self.assertEqual(
            err, err_msg.format(v.__class__.__name__, v.pk))

    def test_get_document(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")
        err = create_document(v)
        self.assertIsNone(err)
        doc = get_document(v)
        self.assertTrue(isinstance(doc, dict))

    def test_get_document_not_found(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")
        with self.assertRaises(DocumentNotFound):
            get_document(v)

    def test_update_document(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")
        doc = get_document(v)
        self.assertTrue(isinstance(doc, dict))

        v.title = "Legit Video, Bruh"
        v.save()
        doc = get_document(v)
        self.assertEqual(doc['_source']['title'], "Legit Video, Bruh")

    def test_delete_document(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")
        err = create_document(v)
        self.assertIsNone(err)
        doc = get_document(v)
        self.assertTrue(isinstance(doc, dict))
        delete_document(v)
        with self.assertRaises(DocumentNotFound):
            get_document(v)

    def test_delete_document_not_found(self):
        app_config = apps.get_app_config('videos')
        create_index(app_config, 'Video')
        self.assertTrue(index_exists(Video.get_index_name()))
        time.sleep(1)
        v = Video.objects.create(
            title="Test Video",
            video_id="Leg1tVid1D",
            thumbnail_url="http://example.com/legitthumbnail.jpeg")

        with self.assertRaises(DocumentNotFound):
            delete_document(v)
