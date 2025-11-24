"""
OrderItem data model
"""
from database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from datetime import datetime

class OrderItem(db.Model):
    """Order item model representing items in an order"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)  # Price at time of order
    customizations = Column(JSON)  # Store selected customization options
    item_total = Column(Float, nullable=False)  # quantity * unit_price
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship - use joined loading to avoid detached instance errors
    menu_item = db.relationship('MenuItem', backref='order_items', lazy='joined')
    
    def to_dict(self):
        """Convert model to dictionary"""
        # Handle detached instance by checking if menu_item is accessible
        menu_item_dict = None
        try:
            if self.menu_item:
                menu_item_dict = self.menu_item.to_dict()
        except Exception:
            # If menu_item is detached, just use menu_item_id
            pass
        
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'menu_item': menu_item_dict,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'customizations': self.customizations or {},
            'item_total': self.item_total
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id} - Order {self.order_id}>'

