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
        "issued_on", "issued_by", "issuing_branch", "serial_no",
        "job_no", "csr", "claim_no", "vehicle_no", "date_and_time_of_accident",
        "accident_location", "insured_full_name", "address", "position", "telephone_no", "registered_owner",
        "full_name_of_the_driver", "licence_number", "date_of_expiry", "relationship",
        "goods_in_vehicle_with_weight", "employees_in_own_vehicle", "date", "email"
    ]
    return f"You are a document-processing specialist AI. Extract the following fields: {', '.join(fields)}. Provide the output in JSON format."
