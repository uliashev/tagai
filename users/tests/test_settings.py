from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SettingsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        self.url = reverse('settings')

    def test_settings_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings.html')
        self.assertContains(response, 'Gemini')
        self.assertContains(response, 'Openai')
        self.assertContains(response, 'submit_gemini')
        self.assertContains(response, 'submit_openai')
        self.assertContains(response, 'LLM model')

    def test_gemini_update(self):
        data = {
            'submit_gemini': 'Save',
            'gemini_api_key': 'test_gemini_key',
            'gemini_model': 'gemini-pro',
            'gemini_prompt': 'test_gemini_prompt'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.gemini_api_key, 'test_gemini_key')
        self.assertEqual(self.user.gemini_model, 'gemini-pro')
        self.assertEqual(self.user.gemini_prompt, 'test_gemini_prompt')
        # OpenAI fields should be unchanged
        self.assertIsNone(self.user.openai_api_key)

    def test_openai_update(self):
        data = {
            'submit_openai': 'Save',
            'openai_api_key': 'test_openai_key',
            'openai_model': 'gpt-4',
            'openai_prompt': 'test_openai_prompt'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.openai_api_key, 'test_openai_key')
        self.assertEqual(self.user.openai_model, 'gpt-4')
        self.assertEqual(self.user.openai_prompt, 'test_openai_prompt')
        # Gemini fields should be unchanged
        self.assertIsNone(self.user.gemini_api_key)

    def test_long_input(self):
        long_string = 'a' * 999
        data = {
            'submit_gemini': 'Save',
            'gemini_api_key': 'short_key',
            'gemini_prompt': long_string
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.gemini_prompt, long_string)
