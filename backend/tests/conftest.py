"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from database import db
from config_test import TestConfig
from models.menu_item import MenuItem
from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment

@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    # Initialize database with test config
    db.init_app(app)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.menu_routes import menu_bp
    from routes.order_routes import order_bp
    from routes.payment_routes import payment_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Fast Food Ordering System API'}, 200
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

import pytest
from datetime import datetime
from your_app.models import MenuItem, db  # adjust import paths

@pytest.fixture(scope='function')
def sample_menu_items(app):
    """Create sample menu items for testing"""
    with app.app_context():
        items = [
            MenuItem(
                name="Classic Burger",
                description="Juicy beef patty",
                price=8.99,
                category="Burgers"
            ),
            MenuItem(
                name="French Fries",
                description="Crispy golden fries",
                price=3.99,
                category="Sides"
            ),
            MenuItem(
                name="Coca Cola",
                description="Refreshing cola drink",
                price=2.49,
                category="Drinks"
            ),
        ]
        
        for item in items:
            db.session.add(item)
        db.session.commit()
        
        # Make items accessible by storing IDs and re-querying when needed
        item_ids = [item.id for item in items]
        
        # List-like object that re-queries items when accessed
        class FreshMenuItems:
            def __init__(self, app_instance, ids):
                self.app = app_instance
                self.ids = ids
            
            def __getitem__(self, index):
                with self.app.app_context():
                    return MenuItem.query.get(self.ids[index])
            
            def __iter__(self):
                with self.app.app_context():
                    for item_id in self.ids:
                        yield MenuItem.query.get(item_id)
            
            def __len__(self):
                return len(self.ids)
        
        return FreshMenuItems(app, item_ids)


