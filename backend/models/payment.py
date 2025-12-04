"""
Payment data model
"""
from database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from datetime import datetime
import enum


class Payment(db.Model):
    """Payment model representing payment transactions"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50))
    processed_at = Column(DateTime)
    
    def to_dict(self):
        """Convert model to dictionary matching frontend types"""
        return {
            'id': str(self.id),
            'orderId': str(self.order_id),
            'amount': self.amount,
            'method': self.payment_method,
            'paidAt': self.processed_at.isoformat() if self.processed_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - Order {self.order_id}>'

