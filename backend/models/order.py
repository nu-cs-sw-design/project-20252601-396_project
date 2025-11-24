"""
Order data model
"""
from database import db
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from datetime import datetime
import enum

class OrderStatus(enum.Enum):
    """Order status enumeration"""
    PENDING = "Pending"
    IN_PREPARATION = "In Preparation"
    READY = "Ready"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class PaymentStatus(enum.Enum):
    """Payment status enumeration"""
    PENDING = "Pending"
    PENDING_COUNTER = "Pending Payment at Counter"
    PAID = "Paid"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class Order(db.Model):
    """Order model representing customer orders"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    status = Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    payment_status = Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)
    tax = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    payment_method = Column(String(50))  # 'card_at_system', 'cash_at_counter', 'card_at_counter'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'status': self.status.value if self.status else None,
            'payment_status': self.payment_status.value if self.payment_status else None,
            'subtotal': self.subtotal,
            'tax': self.tax,
            'total': self.total,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'order_items': [item.to_dict() for item in self.order_items],
            'payments': [payment.to_dict() for payment in self.payments]
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

