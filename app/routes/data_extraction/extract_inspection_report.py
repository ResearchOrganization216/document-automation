from flask import Blueprint, request, jsonify
from pathlib import Path
from app.services.data_extraction.extract_inspection_report_service import process_extraction

extract_bp_inspection_report = Blueprint('extract_bp_inspection_report', __name__)

@extract_bp_inspection_report.route('/extract-inspection-report', methods=['POST'])
def extract_info():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    user_prompt = request.form.get(
        'user_prompt', 
        "Extract key information in JSON format as per the insurance document schema."
    )

    # Save the uploaded image temporarily
    image_path = Path('temp_image.jpeg')
    image_file.save(image_path)

    try:
        output = process_extraction(str(image_path), user_prompt)
        if output.get('error'):
            return jsonify({"error": output['error']}), 500
        return jsonify({"output": output}), 200
    finally:
        if image_path.exists():
            image_path.unlink()
