from flask import Blueprint, request, jsonify
from app.services.document_classification.document_matcher_new import feature_based_matching, load_templates
import os
import tempfile

# Define the blueprint
document_classification_bp = Blueprint('document_classification', __name__)

@document_classification_bp.route('/classify-new', methods=['POST'])
def classify_documents():
    """
    Endpoint to classify one or more uploaded documents.
    """
    if 'documents' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist('documents')
    if not files:
        return jsonify({"error": "No documents provided"}), 400

    results = []
    try:
        templates = load_templates()
        for file in files:
            # Save the file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file.save(temp_file.name)
                temp_file.close()

                # Perform classification
                result = feature_based_matching(temp_file.name, templates)
                result["filename"] = file.filename
                results.append(result)

                # Clean up the temporary file
                os.unlink(temp_file.name)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
