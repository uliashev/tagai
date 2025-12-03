import logging

import exiftool

logger = logging.getLogger(__name__)

import os
import shutil
from django.conf import settings

def write_metadata_to_image(image_path, metadata):
    logger.info(f"Attempting to write metadata to {image_path}...")
    
    # Define target directory and file path
    # Use the directory of the input image to ensure user isolation
    target_dir = os.path.join(os.path.dirname(image_path), 'discribed_gemini')
    os.makedirs(target_dir, exist_ok=True)
    new_image_path = os.path.join(target_dir, os.path.basename(image_path))

    try:
        # Copy original file to new location
        shutil.copy2(image_path, new_image_path)
        logger.info(f"Copied {image_path} to {new_image_path}")

        title = metadata.get("title", "")
        description = metadata.get("description", "")
        keywords = metadata.get("keywords", [])

        with exiftool.ExifTool() as et:
            # Build a list of command-line arguments for ExifTool.
            # All arguments must be passed as bytes.
            params = [
                b"-overwrite_original",  # Prevent creating backup files
                f"-XMP:Title={title}".encode('utf-8'),
                f"-IPTC:ObjectName={title}".encode('utf-8'),
                f"-XMP:Description={description}".encode('utf-8'),
                f"-IPTC:Caption-Abstract={description}".encode('utf-8'),
                # Clear existing keywords/subjects to ensure a clean write
                b"-IPTC:Keywords=",
                b"-XMP:Subject=",
            ]
            # Add each keyword as a separate argument
            for keyword in keywords:
                params.append(f"-IPTC:Keywords={keyword}".encode('utf-8'))
                params.append(f"-XMP:Subject={keyword}".encode('utf-8'))

            # Add the NEW image path as the final argument
            params.append(new_image_path.encode('utf-8'))

            et.execute(*params)

        logger.info(f"Successfully wrote metadata to {new_image_path}")
        
        # Remove the original file after successful write
        if os.path.exists(image_path):
            os.remove(image_path)
            logger.info(f"Removed original file: {image_path}")
            
        return True
    except FileNotFoundError:
        logger.error("ExifTool not found. Please ensure it is installed and in your system's PATH.")
        # Cleanup copy if it exists and failed
        if os.path.exists(new_image_path):
            os.remove(new_image_path)
        return False
    except Exception:
        logger.exception(f"Failed to write metadata to {new_image_path}")
        # Cleanup copy if it exists and failed
        if os.path.exists(new_image_path):
            os.remove(new_image_path)
        return False
