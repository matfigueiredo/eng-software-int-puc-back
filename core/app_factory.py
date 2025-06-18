from flask import Flask
from flask_cors import CORS

from logger import log_info, setup_logger
from routers.prediction import prediction_bp
from services.prediction_service import prediction_service


def create_app() -> Flask:
    """Flask application factory"""
    
    # Setup logger
    setup_logger()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure CORS with explicit settings
    CORS(app, 
         origins=["*"],
         methods=["GET", "POST", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "Accept"],
         supports_credentials=True,
         max_age=86400)  # Cache preflight for 24 hours
    
    # Add explicit OPTIONS handler for all routes
    @app.before_request
    def handle_preflight():
        from flask import request
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            headers = response.headers
            headers['Access-Control-Allow-Origin'] = '*'
            headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
            headers['Access-Control-Max-Age'] = '86400'
            return response
    
    # Register blueprints
    app.register_blueprint(prediction_bp)
    
    # Initialize services on startup
    with app.app_context():
        log_info("🚀 Starting up Flask app...")
        prediction_service.load_model()
    
    @app.teardown_appcontext
    def cleanup(error):
        """Cleanup on app shutdown"""
        if error:
            log_info(f"App error: {error}")
        log_info("🛑 App context teardown...")
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return {"error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return {"error": "Internal server error"}, 500
    
    return app 