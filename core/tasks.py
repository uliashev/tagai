from celery import shared_task
from google.api_core.exceptions import ResourceExhausted
from core.services.google import generate_stock_metadata
from core.services.process_metadata import write_metadata_to_image
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth import get_user_model

User = get_user_model()

import shutil
import os

@shared_task(bind=True, max_retries=None, rate_limit='2/m')
def process_file_task(self, file_path, user_id):
    """
    Process a single file:
    1. Generate metadata using Google service.
    2. Write metadata to the image.
    """
    def mark_as_failed(path):
        try:
            # Rename to .failed if not already
            if not path.endswith('.failed'):
                failed_path = path + '.failed'
                os.rename(path, failed_path)
                logger.info(f"Marked file as failed: {path} -> {failed_path}")
        except Exception as err:
            logger.error(f"Failed to mark file {path} as failed: {err}")

    try:
        logger.info(f"Starting processing for file: {file_path} with user_id: {user_id}")
        
        user = User.objects.get(id=user_id)
        
        # Step 1: Generate metadata
        try:
            metadata = generate_stock_metadata(file_path, user)
        except ResourceExhausted as e:
            logger.warning(f"Rate limit exceeded for {file_path}. Retrying in 30 seconds...")
            raise self.retry(exc=e, countdown=30)

        logger.info(f"Metadata generated for {file_path}: {metadata}")
        
        if metadata and "error" in metadata:
            logger.error(f"Error generating metadata for {file_path}: {metadata['error']}")
            mark_as_failed(file_path)
            return f"Error: {metadata['error']}"
        
        if not metadata:
             logger.error(f"Failed to generate metadata for {file_path}")
             mark_as_failed(file_path)
             return f"Failed to generate metadata for {file_path}"

        # Step 2: Write metadata to image
        if not write_metadata_to_image(file_path, metadata):
            logger.error(f"Failed to write metadata to {file_path}")
            mark_as_failed(file_path)
            return f"Failed to write metadata to {file_path}"
        
        logger.info(f"Successfully processed file: {file_path}")
        return f"Processed {file_path}"
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found.")
        return f"User {user_id} not found"
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
        # Mark as failed so it doesn't block the queue/UI
        mark_as_failed(file_path)
        # Do not re-raise generic exceptions to prevent infinite retries if not intended
        return f"Error: {str(e)}"
