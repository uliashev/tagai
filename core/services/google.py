import json
import logging
import google.generativeai as genai
from PIL import Image
import exiftool
import os

logger = logging.getLogger(__name__)


def generate_stock_metadata(image_path):
    logger.info(f"--- Processing file: {image_path} ---")
    if not os.path.exists(image_path):
        logger.error(f"File not found: {image_path}")
        return None
    try:
        logger.info("Opening image for inline processing...")
        img = Image.open(image_path)

        model = genai.GenerativeModel(LLM)

        logger.info("Generating description and keywords...")
        response = model.generate_content(
            [ADOBE_PROMPT, img],
            generation_config={"response_mime_type": "application/json"}
        )
        json_data = json.loads(response.text)
        logger.info("Successfully generated metadata.")
        return json_data
    except Exception:
        logger.exception("An error occurred during metadata generation.")
        return None
