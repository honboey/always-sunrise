from django.test import TestCase
from ..templatetags.custom_tags import extract_youtube_id


class TemplateTagTests(TestCase):
    def test_extract_youtube_id(self):
        id = extract_youtube_id("https://www.youtube.com/watch?v=GSmCh4DrbWY")
        self.assertEqual(id, "GSmCh4DrbWY")
