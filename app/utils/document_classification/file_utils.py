import os
import uuid

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_files(files):
    saved_files = []
    for file in files:
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        saved_files.append(filepath)
    return saved_files

def cleanup_files(filepaths):
    for filepath in filepaths:
        if os.path.exists(filepath):
            os.remove(filepath)
