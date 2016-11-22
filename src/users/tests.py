from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User


class TestUsersViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_pwd')

    def test_log_in(self):
        url = resolve_url('/users/login/')
        response = self.client.get(url)
        self.assertTrue(response.wsgi_request.user.is_anonymous())
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data={'username': 'test_user', 'password': 'test_pwd'})
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_log_out(self):
        url = resolve_url('/users/login/')
        response = self.client.post(url, data={'username': 'test_user', 'password': 'test_pwd'})
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        url = resolve_url('/users/logout/')
        response = self.client.post(url, user=self.user)
        self.assertTrue(response.wsgi_request.user.is_anonymous())
        self.assertRedirects(response, '/')

    def test_profile_view(self):
        self.client.login(username='test_user', password='test_pwd')
        url = resolve_url('/users/profile/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_view(self):
        self.client.login(username='test_user', password='test_pwd')
        url = resolve_url('/users/profile/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCreateView(TestCase):
    def setUp(self):
        self.url = resolve_url('users/register/')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            'username': 'test_user_2000',
            'password': 'test_pwd',
            'email': 'test@test.com'
        }
        self.client.post(self.url, data=data)
        self.assertTrue(User.objects.filter(username='test_user_2000').exists())
        logged = self.client.login(username='test_user_2000', password='test_pwd')
        self.assertTrue(logged)
        self.assertTrue(User.objects.get(username='test_user_2000').is_authenticated())
