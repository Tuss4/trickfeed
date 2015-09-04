from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class TrickerTests(APITestCase):

    create_url = reverse("register_tricker")

    def test_create_tricker(self):
        response = self.client.post(self.create_url, {
            "email": "youngtricklord@trickhouse.io",
            "password": "butterflytwistround"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tricker_bad_request(self):
        response = self.client.post(self.create_url, {
            "email": "youngtricklord",
            "password": "butterflytwistround"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tricker_conflict(self):
        response = self.client.post(self.create_url, {
            "email": "youngtricklord@trickhouse.io",
            "password": "butterflytwistround"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.create_url, {
            "email": "youngtricklord@trickhouse.io",
            "password": "butterflytwistround"
        })
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
