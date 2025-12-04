"""
MenuItem data model
"""
from database import db
from sqlalchemy import Column, Integer, String, Float, Text, JSON, Boolean, DateTime
from datetime import datetime

class MenuItem(db.Model):
    """Menu item model representing food items in the menu"""
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary matching frontend types"""
        return {
            'id': str(self.id),
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'description': self.description or ''
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'
