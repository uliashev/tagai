import shutil
import tempfile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from pathlib import Path

User = get_user_model()

@override_settings(TEMP_UPLOAD_DIR=Path(tempfile.mkdtemp()))
class FileListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.url = reverse('file_list')
        
        # Create some dummy files
        self.upload_dir = settings.TEMP_UPLOAD_DIR / str(self.user.id)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        (self.upload_dir / "test1.txt").touch()
        (self.upload_dir / "test2.jpg").touch()

    def tearDown(self):
        # Clean up temp dir
        if settings.TEMP_UPLOAD_DIR.exists():
            shutil.rmtree(settings.TEMP_UPLOAD_DIR, ignore_errors=True)

    def test_file_list_view(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/files.html')
        self.assertContains(response, "test1.txt")
        self.assertContains(response, "test2.jpg")
        
    def test_file_list_empty(self):
        # Clear files
        for f in self.upload_dir.iterdir():
            f.unlink()
            
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No files uploaded yet")

    def test_user_isolation(self):
        # Create another user and upload a file
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_user_dir = settings.TEMP_UPLOAD_DIR / str(other_user.id)
        other_user_dir.mkdir(parents=True, exist_ok=True)
        (other_user_dir / "other_user_file.txt").touch()
        
        # Log in as the original user
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "other_user_file.txt")
        self.assertContains(response, "test1.txt")
