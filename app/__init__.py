from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Loading configuration
    app.config.from_object('config.Config')

    # Initializing extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registering blueprints
    from app.routes.data_extraction.extract_claim_report_info import extract_bp_claim_report
    from app.routes.data_extraction.extract_driver_statememt_info import extract_bp_driver_statement
    from app.routes.data_extraction.extract_inspection_report import extract_bp_inspection_report
    #from app.routes.document_classification.document_classification import document_classification_bp
    from app.routes.document_classification.extract_document_classification import extract_bp_document_classification


    app.register_blueprint(extract_bp_claim_report, url_prefix='/api')
    app.register_blueprint(extract_bp_driver_statement, url_prefix='/api')
    app.register_blueprint(extract_bp_inspection_report, url_prefix='/api')
    #app.register_blueprint(document_classification_bp, url_prefix='/api') #new route for document classification using opencv
    app.register_blueprint(extract_bp_document_classification, url_prefix='/api') #new route for document classification using LLM


    # Default route for '/'
    @app.route('/')
    def index():
        return "Welcome to Flask with PostgreSQL!"

    return app
