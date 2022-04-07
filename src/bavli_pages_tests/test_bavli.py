from unittest import TestCase
import bavli_pages as bp


class TestBavli(TestCase):

    def all_pages_test(self):
        bp._get_bavli_obj().all_pages_in_each_chapter()

    def all_chapters_test(self):
        bp._get_bavli_obj().generate_chapter_view()
