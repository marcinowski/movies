from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from django.conf import settings


class TestMainView(TestCase):
    def setUp(self):
        self.url = resolve_url('/')
        self.user = User.objects.create_user(username='test_user', password='test_pwd')

    def test_main_page_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_main_page_authenticated(self):
        title = 'test'
        logged = self.client.login(username='test_user', password='test_pwd')
        self.assertTrue(logged)
        response = self.client.post(self.url, data={'title': title})
        self.assertRedirects(
            response,
            expected_url='/movie_list/?title=test'
        )

    def test_post_main_page_not_authenticted(self):
        title = 'test'
        response = self.client.post(self.url, data={'title': title})
        self.assertRedirects(response, settings.LOGIN_URL + '?next=' + settings.LOGIN_REDIRECT_URL)
