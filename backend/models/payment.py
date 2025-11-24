"""
Payment data model
"""
from database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from datetime import datetime
import enum

class PaymentStatus(enum.Enum):
    """Payment status enumeration"""
    PENDING = "Pending"
    PROCESSING = "Processing"
    APPROVED = "Approved"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class PaymentMethod(enum.Enum):
    """Payment method enumeration"""
    CARD_AT_SYSTEM = "card_at_system"
    CASH_AT_COUNTER = "cash_at_counter"
    CARD_AT_COUNTER = "card_at_counter"

class Payment(db.Model):
    """Payment model representing payment transactions"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(db.Enum(PaymentMethod), nullable=False)
    status = Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    transaction_id = Column(String(100))  # External payment processor transaction ID
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'status': self.status.value if self.status else None,
            'transaction_id': self.transaction_id,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - Order {self.order_id}>'

