from pathlib import Path
import logging
import google.generativeai as genai
import os

# Configure Google API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found in environment variables.")
genai.configure(api_key=GOOGLE_API_KEY)

# Model Configuration
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=MODEL_CONFIG
)

def image_format(image_path):
    img = Path(image_path)
    if not img.exists():
        logging.error(f"Image not found at {img}")
        raise FileNotFoundError(f"Image not found at {img}")
    return [{"mime_type": "image/jpeg", "data": img.read_bytes()}]

def gemini_classification(image_path, user_prompt):
    try:
        image_info = image_format(image_path)
        dynamic_prompt = (
            "You are a document-classifying AI. Analyze the document and classify it as either "
            "a claim_report, inspection_report, repair_estimate, or driver_statement. Provide the classification result."
        )
        input_prompt = [dynamic_prompt, image_info[0], user_prompt]
        response = model.generate_content(input_prompt)
        return response.text if response and response.text else None
    except Exception as e:
        logging.error(f"Error generating classification: {e}")
        return None

def process_classification(image_path, user_prompt):
    output = gemini_classification(image_path, user_prompt)
    if not output:
        return {"error": "Failed to generate output from LLM."}
    return {"classification": output}
