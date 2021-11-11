from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_page_uses_correct_template(self):
        """При запросе к about/*
        применяется шаблон about/*.html."""
        templates_page_names = {
            'author.html': reverse('author'),
            'tech.html': reverse('tech')
        }

        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
