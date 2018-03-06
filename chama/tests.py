from __future__ import unicode_literals
from __future__ import absolute_import
from django.test import TestCase
from django.urls import resolve
from chama.views import index


class IndexTest(TestCase):
    def test_root_url_resolves_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
