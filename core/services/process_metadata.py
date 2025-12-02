import logging

logger = logging.getLogger(__name__)

def write_metadata_to_image(image_path, metadata):
    logger.info('Writing metadata to image')