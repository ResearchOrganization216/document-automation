import google.generativeai as genai
import os
import logging
import json
import jsonschema
import re
from app.utils.data_extraction.extract_driver_statement_utils import image_format, get_dynamic_prompt

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

# Safety settings
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=SAFETY_SETTINGS,
    generation_config=MODEL_CONFIG
)

# JSON Schema for Validation
json_schema = {
    "type": "object",
    "properties": {
        "vehicle_no": {"type": "string"},
        "date_and_time": {"type": "string", "format": "date"},
        "accident_location": {"type": "string"},
        "driver_name": {"type": "string"},
        "driver_nic": {"type": "string"},
        "driver_occupation": {"type": "string"}, 
        "purpose_of_journey": {"type": "string"},
        "name_of_vehicle_owner": {"type": "string"},
        "relationship": {"type": "string"}, 
        "no_of_passengers": {"type": "string"}
    },
    "required": ["vehicle_no", "date_and_time", "accident_location", "driver_name",
        "driver_nic", "driver_occupation", "purpose_of_journey", "name_of_vehicle_owner", "relationship",
        "no_of_passengers"]
}


def gemini_output(image_path, user_prompt):
    try:
        image_info = image_format(image_path)
        dynamic_prompt = get_dynamic_prompt()
        input_prompt = [dynamic_prompt, image_info[0], user_prompt]
        response = model.generate_content(input_prompt)
        return response.text if response and response.text else None
    except Exception as e:
        logging.error(f"Error generating content: {e}")
        return None

def preprocess_output(parsed_output):
    for key, value in parsed_output.items():
        if value is None:
            parsed_output[key] = ""
    return parsed_output

def parse_json_fallback(output_text):
    json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            logging.error("Fallback parsing failed, invalid JSON structure.")
    return None

def process_extraction(image_path, user_prompt):
    output = gemini_output(image_path, user_prompt)
    if not output:
        return {"error": "Failed to generate output from LLM."}

    try:
        parsed_output = json.loads(output)
    except json.JSONDecodeError:
        parsed_output = parse_json_fallback(output)

    if parsed_output:
        parsed_output = preprocess_output(parsed_output)
        try:
            jsonschema.validate(instance=parsed_output, schema=json_schema)
            return parsed_output
        except jsonschema.ValidationError as e:
            return {"error": "Validation failed.", "details": str(e)}
    return {"error": "Parsing failed."}
