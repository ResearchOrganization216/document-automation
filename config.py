import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@34.142.174.193:5432/InnoAInsure'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUCKET_NAME = "innoainsure-bucket" 
     # For local development, provide a key file; in production, you can set this to an empty string or None.
    #KEY_PATH = "C:\Users\Administrator\Documents\keyfiles\\proven-answer-451215-k1-190fdb8da7df.json"
    KEY_PATH = ""  # Set to an empty string in production
    PROJECT_ID = "proven-answer-451215-k1"
    SECRET_KEY = 'your-very-secret-key'