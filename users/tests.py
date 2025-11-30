from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_form_fields(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Password')
        self.assertNotContains(response, 'Forgot Password')

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        # Should redirect after successful login. 
        # Since we didn't set LOGIN_REDIRECT_URL, it might default to /accounts/profile/ or similar.
        # But for now, just checking it redirects (302) is enough to prove auth worked.
        self.assertEqual(response.status_code, 302) 

    def test_login_failure(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_home_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_home_renders_dashboard_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/dashboard.html')
