import json
import logging
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument, ResourceExhausted
from PIL import Image
import exiftool
import os

logger = logging.getLogger(__name__)


def generate_stock_metadata(image_path, user):
    logger.info(f"--- Processing file: {image_path} ---")
    if not os.path.exists(image_path):
        logger.error(f"File not found: {image_path}")
        return None
    
    if not user.gemini_api_key:
        logger.error("Gemini API key not found for user.")
        return None
        
    try:
        genai.configure(api_key=user.gemini_api_key)
        
        logger.info("Opening image for inline processing...")
        img = Image.open(image_path)

        model_name = user.gemini_model if user.gemini_model else "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)

        prompt = user.gemini_prompt if user.gemini_prompt else "Describe this image."

        logger.info(f"Generating description and keywords using model: {model_name}")
        response = model.generate_content(
            [prompt, img],
            generation_config={"response_mime_type": "application/json"}
        )
        json_data = json.loads(response.text)
        logger.info("Successfully generated metadata.")
        return json_data
    except InvalidArgument as e:
        logger.error(f"Invalid API Key provided: {e}")
        return {"error": "Invalid API Key. Please check your settings."}
    except ResourceExhausted:
        # Re-raise to allow Celery to handle retries
        logger.warning("Quota exceeded. Re-raising ResourceExhausted for retry.")
        raise
    except Exception:
        logger.exception("An error occurred during metadata generation.")
        return None
