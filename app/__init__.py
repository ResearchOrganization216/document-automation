from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Loading configuration
    app.config.from_object('app.config.Config')

    # Initializing extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registering blueprints
    #from app.routes.claims import claims_bp
    #from app.routes.customer_risk_prediction.customer_risk_prediction import customer_risk_bp
    #from app.routes.data_extraction.extract_claim_report_info import extract_bp_claim_report
    #from app.routes.data_extraction.extract_driver_statememt_info import extract_bp_driver_statement
    #from app.routes.data_extraction.extract_inspection_report import extract_bp_inspection_report
    #from app.routes.document_classification.document_classification import document_classification_bp
    #from app.routes.document_classification.extract_document_classification import extract_bp_document_classification
    #from app.routes.customer_risk_assesment.risk_assesment import risk_assessment_bp
    #from app.routes.customer_risk_agent.risk_routes import risk_bp
    #from app.routes.customer_risk_assesment_llama.risk_assesment_llama import risk_assesment_llama_bp
    #from app.routes.customer_risk_assesment_openai.risk_assesment_openai import risk_assessment_openai_bp


    #app.register_blueprint(claims_bp, url_prefix='/api/claims')
    #app.register_blueprint(customer_risk_bp, url_prefix='/api')
    #app.register_blueprint(extract_bp_claim_report, url_prefix='/api')
    #app.register_blueprint(extract_bp_driver_statement, url_prefix='/api')
    #app.register_blueprint(extract_bp_inspection_report, url_prefix='/api')
    #app.register_blueprint(document_classification_bp, url_prefix='/api') #new route for document classification using opencv
    #app.register_blueprint(extract_bp_document_classification, url_prefix='/api') #new route for document classification using LLM
    #app.register_blueprint(risk_assessment_bp, url_prefix='/api') #new route for risk assesment using LLM
    #app.register_blueprint(risk_bp, url_prefix='/api') #new route for risk assesment using Agent
    #app.register_blueprint(risk_assesment_llama_bp, url_prefix='/api') #new route for risk assesment using
    #app.register_blueprint(risk_assessment_openai_bp, url_prefix='/api') #new route for risk assesment using OpenAI

    # Default route for '/'
    @app.route('/')
    def index():
        return "Welcome to Flask with PostgreSQL!"

    return app
