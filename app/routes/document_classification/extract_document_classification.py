from flask import Blueprint, request, jsonify
from pathlib import Path
from app.services.document_classification.extract_document_classification import process_classification

extract_bp_document_classification = Blueprint('extract_bp_document_classification', __name__)

@extract_bp_document_classification.route('/classify-document', methods=['POST'])
def classify_document():
    if 'images' not in request.files:
        return jsonify({"error": "No images provided"}), 400

    images = request.files.getlist('images')  # Get the list of uploaded images
    user_prompt = request.form.get(
        'user_prompt', 
        "Classify the document as one of the following types: claim report, inspection report, repair estimate, driver statement."
    )

    results = []  # Store results for all classified documents

    for image_file in images:
        # Save the uploaded image temporarily
        image_path = Path(f'temp_image_classification_{image_file.filename}')
        image_file.save(image_path)

        try:
            classification_result = process_classification(str(image_path), user_prompt)
            if classification_result.get('error'):
                return jsonify({"error": classification_result['error']}), 500
            
            # Append the classification result with filename to the results list
            results.append({
                "document_type": classification_result["classification"],
                "filename": image_file.filename,
            })
        finally:
            if image_path.exists():
                image_path.unlink()  # Remove the temporary image file

    return jsonify(results), 200  # Return the results in the specified format
