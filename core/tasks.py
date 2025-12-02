from celery import shared_task
from core.services.google import generate_stock_metadata
from core.services.process_metadata import write_metadata_to_image
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_file_task(file_path):
    """
    Process a single file:
    1. Generate metadata using Google service.
    2. Write metadata to the image.
    """
    try:
        logger.info(f"Starting processing for file: {file_path}")
        
        # Step 1: Generate metadata
        metadata = generate_stock_metadata(file_path)
        
        # Step 2: Write metadata to image
        write_metadata_to_image(file_path, metadata)
        
        logger.info(f"Successfully processed file: {file_path}")
        return f"Processed {file_path}"
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
        raise e
