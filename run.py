from app import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
