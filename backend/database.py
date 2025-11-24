"""
Database configuration and initialization
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Import all models here to ensure they're registered
        from models.menu_item import MenuItem
        from models.order import Order
        from models.order_item import OrderItem
        from models.payment import Payment
        
        # Create all tables
        db.create_all()
    
    return db

