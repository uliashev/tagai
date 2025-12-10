# import base64
# import json
# import logging
# import os
#
# from openai import OpenAI
# from pytest_django.fixtures import client
#
# logger = logging.getLogger(__name__)
#
#
#
# def generate_stock_metadata(image_path: str, user):
#     logger.info(f"--- Processing file: {image_path} ---")
#     if not os.path.exists(image_path):
#         logger.error(f"File not found: {image_path}")
#         return None
#
#     if not user.gemini_api_key:
#         logger.error("OpenAI API key not found for user.")
#         return None
#
#     with open(image_path, "rb") as img:
#         image_bytes = img.read()
#
#     b64 = base64.b64encode(image_bytes).decode("utf-8")
#
#     data_url = f"data:image/jpeg;base64,{b64}"
#     client = OpenAI(api_key=user.openai_api_key)
#     model = user.openai_model if user.openai_model else "gpt-4.1"
#     prompt = user.openai_prompt if user.openai_prompt else "Describe this image."
#
#
#     response = client.responses.create(
#         model=model,
#         input=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "input_text",
#                         "text": prompt
#                     },
#                     {
#                         "type": "input_image",
#                         "image_url": data_url
#                     }
#                 ]
#             }
#         ]
#     )
#
#     return response.to_dict()
#
#
#
# # if __name__ == "__main__":
# #     model = "gpt-4.1"
# #     result = generate_stock_metadata(
# #         file_path="/home/danaro/repo/tagai/temp_uploads/1.jpg",
# #         prompt=prompt,
# #         model=model
# #     )
# #
# #     print(json.dumps(result, indent=4, ensure_ascii=False))
