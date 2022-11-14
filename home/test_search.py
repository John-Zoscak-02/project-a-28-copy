from django.test import TestCase


class SearchPageSetUpTest(TestCase):
    def open_search_page(self):
        response = self.client.get('/search')
        self.assertEquals(response.status_code, 200)