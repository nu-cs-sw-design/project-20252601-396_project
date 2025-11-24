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
    category = Column(String(50), nullable=False)  # e.g., 'Burgers', 'Sides', 'Drinks'
    image_url = Column(String(255))
    customization_options = Column(JSON)  # Store available customization options
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'customization_options': self.customization_options or {},
            'is_available': self.is_available
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'
