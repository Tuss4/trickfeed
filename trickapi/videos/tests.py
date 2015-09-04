from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import YT, YT_URL
from trickers.models import Tricker

import datetime


class VideoTests(APITestCase):

    admin_data = {
        "email": "trick_beast@admin.com",
        "password": "Password1"
    }

    regular_data = {
        "email": "trick_padawan@tricking.io",
        "password": "snapuswipe"
    }

    video_data = {
        "video_id": "LEGITVIDEOID",
        "video_type": YT,
        "title": "Tricking is Based on Martial Arts",
        "thumbnail_url": "http://example.com/tricking.jpeg"
    }

    video_2_data = {
        "video_type": "YT",
        "title": "Martial Arts Tricking",
        "video_id": "12-5XjY6imQ",
        "thumbnail_url": "https://i.ytimg.com/vi/12-5XjY6imQ/hqdefault.jpg",
    }

    register_url = reverse('register_tricker')
    video_url = reverse('list_videos')
    video_detail = 'video_detail'

    def get_detail_url(self, url_str, *args):
        return reverse(url_str, args=args)

    def setUp(self):
        response = self.client.post(self.register_url, self.admin_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.admin = Tricker.objects.get(pk=response.data['id'])
        self.admin.is_admin = True
        self.admin.save()

        response = self.client.post(self.register_url, self.regular_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.reg = Tricker.objects.get(pk=response.data['id'])

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        response = self.client.post(self.video_url, self.video_2_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

    # Video Creation
    def test_create_video(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        response = self.client.post(self.video_url, self.video_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['video_url'], YT_URL.format(self.video_data['video_id']))
        self.assertEqual(response.data['date_added'], datetime.date.today().strftime("%Y-%m-%d"))
        self.assertEqual(response.data['video_id'], self.video_data['video_id'])
        self.assertEqual(response.data['video_type'], YT)
        self.assertEqual(response.data['title'], self.video_data['title'])
        self.assertEqual(response.data['thumbnail_url'], self.video_data['thumbnail_url'])

    def test_create_video_unauthorized(self):
        response = self.client.post(self.video_url, self.video_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_video_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.reg.auth_token.key)
        response = self.client.post(self.video_url, self.video_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_video_bad_request(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        response = self.client.post(self.video_url, {
            "title": "Bruh Tricking Vol 17",
            "thumbnail": "http://aintgotone.com/jpeg.gif"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_video_integrity_error(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        response = self.client.post(self.video_url, self.video_2_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # Video Detail
