# utils/gemini_utils.py

import time
import os
from google import genai
from google.genai.errors import ServerError
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
]


def get_gemini_models():
    models = client.models.list()
    valid = []

    for m in models:
        name = m.name

        if "gemini" not in name:
            continue

        if hasattr(m, "supported_actions"):
            if "generateContent" not in m.supported_actions:
                continue

        valid.append(name)

    valid.sort(key=lambda x: ("flash" not in x, x))
    return valid


def call_gemini_with_retry(uploaded_file, prompt, max_retries=3):
    last_error = None
    models_to_try = get_gemini_models()

    while models_to_try:
        model = models_to_try.pop(0)

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[uploaded_file, prompt],
                    config={
                        "response_mime_type": "application/json",
                    },
                )
                return response.text

            except ServerError as e:
                last_error = e
                status_code = getattr(e, "status_code", None)

                if status_code == 503:
                    time.sleep(2**attempt)
                    continue

                if status_code == 404:
                    print(f"[WARN] Model {model} not available. Skipping.")
                    break

                break

            except Exception as e:
                last_error = e
                break

    raise Exception(f"All Gemini models failed. Last error: {last_error}")


def call_gemini_multimodal(file_bytes, prompt, max_retries=3):
    """
    Version optimisée pour envoyer des fichiers binaires (PDF, Images)
    directement à Gemini avec le nouveau SDK.
    """
    last_error = None
    models_to_try = get_gemini_models()

    while models_to_try:
        model = models_to_try.pop(0)

        contents = []
        if file_bytes:
            contents.append(
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type="application/pdf"
                )
            )

        contents.append(prompt)

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config={
                        "response_mime_type": "application/json",
                    },
                )
                return response.text

            except ServerError as e:
                last_error = e
                status_code = getattr(e, "status_code", None)
                if status_code == 503:
                    time.sleep(2**attempt)
                    continue
                break

            except Exception as e:
                last_error = e

                print(f"[DEBUG] Error with model {model}: {e}")
                break

    raise Exception(f"All Gemini models failed multimodal task. Last error: {last_error}")
