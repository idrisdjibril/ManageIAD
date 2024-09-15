from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')

    def test_csrf_protection(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, 403)  # CSRF token missing, should be forbidden

    def test_password_complexity(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'weak',
            'password2': 'weak'
        })
        self.assertFormError(response, 'form', 'password2', 'This password is too short. It must contain at least 8 characters.')

    def test_rate_limiting(self):
        for _ in range(6):  # Attempt to login 6 times (our limit is 5/minute)
            response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 403)  # Should be rate limited

    def test_secure_cookies(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('dashboard_agent'))
        self.assertTrue(response.cookies['sessionid']['secure'])
        self.assertTrue(response.cookies['csrftoken']['secure'])

    def test_xss_protection(self):
        response = self.client.get(reverse('login'), {'next': '<script>alert("XSS")</script>'})
        self.assertNotIn('<script>alert("XSS")</script>', response.content.decode())