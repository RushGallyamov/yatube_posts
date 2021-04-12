from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

USER = get_user_model()


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_loc_for_anonymous(self):
        """
        Страница Технологии  доступна неавторизованному пользователю
        """
        urls = [reverse('about:tech'), reverse('about:author')]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_about_urls_use_correct_template(self):
        """URLs about используют соответсвующий шаблон"""
        expected_pages = {
            reverse('about:tech'): 'about/tech.html',
            reverse('about:author'): 'about/author.html',
        }
        for url, template in expected_pages.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
