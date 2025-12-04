"""
Order data model
"""
from database import db
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from datetime import datetime
import enum

class OrderStatus(enum.Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    PREPARING = 'preparing'
    READY = 'ready'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Order(db.Model):
    """Order model representing customer orders"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary matching frontend types"""
        return {
            'id': str(self.id),
            'items': [item.to_dict() for item in self.order_items],
            'status': self.status.value if self.status else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'payment': self.payment[0].to_dict() if self.payment else None,
            'totalAmount': self.total
        }
    
    def __repr__(self):
        return f'<Order {self.id}>'

