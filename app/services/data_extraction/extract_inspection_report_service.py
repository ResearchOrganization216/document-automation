import google.generativeai as genai
import os
import logging
import json
import jsonschema
import re
from app.utils.data_extraction.extract_inspection_report_utils import image_format, get_dynamic_prompt

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
        "mr_mrs": {"type": "string"},
        "agency_code": {"type": "string"},
        "vehicle_no": {"type": "string"},
        "epf_no": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "time": {"type": "string"}, 
        "name_and_address_of_person": {"type": "string"},
        "make": {"type": "string"}, 
        "year": {"type": "string"},
        "color": {"type": "string"},
        "type": {"type": "string"},
        "engine_no": {"type": "string"},
        "chassis_no": {"type": "string"},
        "vehicle_gasoline": {"type": "string"},
        "paint": {"type": "string"},
        "body_work": {"type": "string"},
        "power_steering": {"type": "string"},
        "air_bags": {"type": "string"},
        "rim_embellisher": {"type": "string"},
        "auto_gear": {"type": "string"},
        "power_winker_mirror": {"type": "string"},
        "abs_brake": {"type": "string"},
        "alloy_wheel_rim": {"type": "string"}, 
        "four_wheel_driver": {"type": "string"},
        "power_shutter": {"type": "string"},
        "power_ariel": {"type": "string"},
        "spoiler": {"type": "string"},
        "modified_buffer": {"type": "string"},
        "single_dual_ac": {"type": "string"},
        "navigation": {"type": "string"},
        "rear_wiper": {"type": "string"},
        "body_kit": {"type": "string"},
        "cassette": {"type": "string"},
        "fog_buffer_lamps": {"type": "string"},
        "hood_railing": {"type": "string"},
        "sun_roof": {"type": "string"},
        "cd_dvd": {"type": "string"},
        "reverse_camera": {"type": "string"}, 
        "remote_smart_key": {"type": "string"},
        "sun_door_wiser": {"type": "string"},
    },
    "required": ["mr_mrs", "agency_code", "vehicle_no", "epf_no", "date", "time",
                "name_and_address_of_person", "make", "year", "color", "type", "engine_no",
                "chassis_no", "vehicle_gasoline", "paint", "body_work", "power_steering", "air_bags", 
                "rim_embellisher", "auto_gear", "power_winker_mirror", "abs_brake", "alloy_wheel_rim", 
                "four_wheel_driver", "power_shutter", "power_ariel", "spoiler", "modified_buffer", "single_dual_ac", 
                "navigation", "rear_wiper", "body_kit", "cassette", "fog_buffer_lamps", "hood_railing", "sun_roof", 
                "cd_dvd", "reverse_camera", "remote_smart_key", "sun_door_wiser"]
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
