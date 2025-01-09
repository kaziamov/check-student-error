from django.test import TestCase


class AppTest(TestCase):

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/articles')
        self.assertContains(response, '/categories')
        self.assertContains(response, '/about')

    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_articles_page(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_categories_page(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
