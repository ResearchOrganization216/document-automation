from pathlib import Path
import logging

def image_format(image_path):
    img = Path(image_path)
    if not img.exists():
        logging.error(f"Image not found at {img}")
        raise FileNotFoundError(f"Image not found at {img}")
    return [{"mime_type": "image/jpeg", "data": img.read_bytes()}]

def get_dynamic_prompt():
    fields = [
        "vehicle_no", "date_and_time", "accident_location", "driver_name",
        "driver_nic", "driver_occupation", "purpose_of_journey", "name_of_vehicle_owner", "relationship",
        "no_of_passengers"
    ]
    return f"You are a document-processing specialist AI. Extract the following fields: {', '.join(fields)}. Provide the output in JSON format."
