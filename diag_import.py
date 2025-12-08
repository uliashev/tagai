# diag_import.py
import os
import django
import sys
import logging

logging.basicConfig(level=logging.INFO)

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Replace 'config.settings' with the actual path to your settings file

try:
    logging.info("Starting Django setup...")
    # This call forces Django to initialize everything
    django.setup()

    # If setup passes, try importing the tasks module
    logging.info("Django setup complete. Attempting to import Celery tasks...")
    # Replace 'core.tasks' with the actual path to your tasks module
    import core.tasks

    logging.info("Import successful. No fatal errors found.")

except Exception as e:
    logging.error("FATAL ERROR during Django import:")
    # Print the full traceback to the Render logs
    import traceback

    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
    