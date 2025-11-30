import shutil
import tempfile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from pathlib import Path

User = get_user_model()

@override_settings(TEMP_UPLOAD_DIR=Path(tempfile.mkdtemp()))
class FileUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.url = reverse('upload_files')

    def tearDown(self):
        # Clean up temp dir
        if settings.TEMP_UPLOAD_DIR.exists():
            shutil.rmtree(settings.TEMP_UPLOAD_DIR, ignore_errors=True)

    def test_upload_files_success(self):
        file1 = SimpleUploadedFile("file1.txt", b"content1")
        file2 = SimpleUploadedFile("file2.txt", b"content2")
        
        response = self.client.post(self.url, {'files': [file1, file2]})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(settings.TEMP_UPLOAD_DIR.exists())
        self.assertTrue((settings.TEMP_UPLOAD_DIR / "file1.txt").exists())
        self.assertTrue((settings.TEMP_UPLOAD_DIR / "file2.txt").exists())

    def test_upload_too_many_files(self):
        files = [SimpleUploadedFile(f"file{i}.txt", b"content") for i in range(21)]
        
        response = self.client.post(self.url, {'files': files})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Maximum 20 files allowed', response.json()['error'])

    def test_upload_no_files(self):
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('No files provided', response.json()['error'])
