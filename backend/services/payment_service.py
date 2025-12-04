"""
Payment Service - Business logic for payment operations
"""
from database import db
from models.order import Order, OrderStatus
from models.payment import Payment
from services.order_service import OrderService
from typing import Optional
from datetime import datetime
import random
import string

class PaymentService:
    """Service for payment-related operations"""
    
    @staticmethod
    def process_payment_at_system(order_id: int, cardInfo: string) -> Payment:
        """
        Process payment at the system (card payment)
        
        Args:
            order_id: ID of the order
            
        Returns:
            Created Payment record
        """
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if order.status != OrderStatus.PENDING:
            raise ValueError(f"Order status is {order.status.value}, cannot process payment")
        
        
        # For now, we'll simulate successful payment
        payment = Payment(
            order_id=order_id,
            amount=order.total,
            payment_method="system_card_" + cardInfo,
            processed_at=datetime.utcnow()
        )
        
        db.session.add(payment)
        
        # Update order status
        order.status = OrderStatus.PAID  # Ready for kitchen
        
        db.session.commit()
        return payment
    
    @staticmethod
    def process_payment_at_counter(order_id: int, payment_method: str) -> Payment:
        """
        Process payment at the counter (cash or card)
        
        Args:
            order_id: ID of the order
            payment_method: 'cash_at_counter' or 'card_at_counter'
            
        Returns:
            Created Payment record
        """
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if order.status != OrderStatus.CONFIRMED:
            raise ValueError(f"Order status is {order.status.value}, cannot process payment")
        
        # Create payment record
        payment = Payment(
            order_id=order_id,
            amount=order.total,
            payment_method=payment_method,
            processed_at=datetime.utcnow()
        )
        
        db.session.add(payment)
        
        # Update order status
        order.status = OrderStatus.PAID 
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        return payment
    
    @staticmethod
    def get_payment_by_order_id(order_id: int) -> Optional[Payment]:
        """Get payment record for an order"""
        return OrderService.get_order_by_id(order_id).payments.first()
    

    
