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

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for React frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Register blueprints
    from routes.main import main_bp
    app.register_blueprint(main_bp)
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Fast Food Ordering System API'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

