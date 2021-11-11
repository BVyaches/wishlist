from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_templates(self):

        '''templates work fine'''
        templates = {

            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }
        for value, expected in templates.items():
            with self.subTest(value=value):
                self.assertTemplateUsed(
                    self.guest_client.get(value), expected)

    def test_about_author_available_for_anonim(self):
        """About author works for anonym"""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech_available_for_anonim(self):
        """About tech works for anonym"""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)