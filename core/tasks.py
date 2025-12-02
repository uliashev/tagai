from celery import shared_task
from core.services.google import generate_stock_metadata
from core.services.process_metadata import write_metadata_to_image
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def process_file_task(file_path, user_id):
    """
    Process a single file:
    1. Generate metadata using Google service.
    2. Write metadata to the image.
    """
    try:
        logger.info(f"Starting processing for file: {file_path} with user_id: {user_id}")
        
        user = User.objects.get(id=user_id)
        
        # Step 1: Generate metadata
        metadata = generate_stock_metadata(file_path, user)
        
        if metadata and "error" in metadata:
            logger.error(f"Error generating metadata for {file_path}: {metadata['error']}")
            return f"Error: {metadata['error']}"
        
        if not metadata:
             logger.error(f"Failed to generate metadata for {file_path}")
             return f"Failed to generate metadata for {file_path}"

        # Step 2: Write metadata to image
        write_metadata_to_image(file_path, metadata)
        
        logger.info(f"Successfully processed file: {file_path}")
        return f"Processed {file_path}"
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found.")
        return f"User {user_id} not found"
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
        raise e
