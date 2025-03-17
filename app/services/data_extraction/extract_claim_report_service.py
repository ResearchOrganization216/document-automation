import google.generativeai as genai
import os
import logging
import json
import jsonschema
import re
from app.utils.data_extraction.extract_claim_report_utils import image_format, get_dynamic_prompt

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
        "issued_on": {"type": "string"},
        "issued_by": {"type": "string"},
        "issuing_branch": {"type": "string"},
        "serial_no": {"type": "string"},
        "job_no": {"type": "string"},
        "csr": {"type": "string"}, 
        "claim_no": {"type": "string", "format": "date"},
        "vehicle_no": {"type": "string", "format": "date"},
        "date_and_time_of_accident": {"type": "string"}, 
        "accident_location": {"type": "string"},
        "insured_full_name": {"type": "string"},
        "address": {"type": "string"},
        "position": {"type": "string"},
        "telephone_no": {"type": "string"},
        "registered_owner": {"type": "string"},
        "full_name_of_the_driver": {"type": "string"},
        "licence_number": {"type": "string"},
        "date_of_expiry": {"type": "string"},
        "relationship": {"type": "string", "format": "date"},
        "goods_in_vehicle_with_weight": {"type": "string"},
        "employees_in_own_vehicle": {"type": "string"},
        "date": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["issued_on", "issued_by", "issuing_branch", "serial_no",
        "job_no", "csr", "claim_no", "vehicle_no", "date_and_time_of_accident",
        "accident_location", "insured_full_name", "address", "position", "telephone_no", "registered_owner",
        "full_name_of_the_driver", "licence_number", "date_of_expiry", "relationship",
        "goods_in_vehicle_with_weight", "employees_in_own_vehicle", "date", "email"]
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
