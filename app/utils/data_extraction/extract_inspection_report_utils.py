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
       "mr_mrs", "agency_code", "vehicle_no", "epf_no", "date", "time",
                "name_and_address_of_person", "make", "year", "color", "type", "engine_no",
                "chassis_no", "vehicle_gasoline", "paint", "body_work", "power_steering", "air_bags", 
                "rim_embellisher", "auto_gear", "power_winker_mirror", "abs_brake", "alloy_wheel_rim", 
                "four_wheel_driver", "power_shutter", "power_ariel", "spoiler", "modified_buffer", "single_dual_ac", 
                "navigation", "rear_wiper", "body_kit", "cassette", "fog_buffer_lamps", "hood_railing", "sun_roof", 
                "cd_dvd", "reverse_camera", "remote_smart_key", "sun_door_wiser"
    ]
    return f"You are a document-processing specialist AI. Extract the following fields: {', '.join(fields)}. Provide the output in JSON format."
