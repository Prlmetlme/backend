from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):
    def setup(self):
        self.client = Client()
        reverse()