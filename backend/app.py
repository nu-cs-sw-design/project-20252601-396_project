"""
Fast Food Ordering System - Flask Backend
Main application entry point
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from config import Config
from database import init_db

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS for React frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.menu_routes import menu_bp
    from routes.order_routes import order_bp
    from routes.payment_routes import payment_bp
    from routes.kitchen_routes import kitchen_bp
    from routes.report_routes import report_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(kitchen_bp)
    app.register_blueprint(report_bp)
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Fast Food Ordering System API'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Use port from environment variable or default to 5001 (5000 is often used by AirPlay on macOS)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

