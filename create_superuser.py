import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username='testadmin').exists():
    User.objects.create_superuser('testadmin', 'admin@example.com', 'testpass123')
    print("Superuser 'testadmin' created.")
else:
    print("Superuser 'testadmin' already exists.")
