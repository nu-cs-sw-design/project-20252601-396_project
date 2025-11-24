"""
Payment Service - Business logic for payment operations
"""
from database import db
from models.payment import Payment, PaymentStatus, PaymentMethod
from models.order import Order, OrderStatus, PaymentStatus as OrderPaymentStatus
from services.order_service import OrderService
from typing import Optional
from datetime import datetime
import random
import string

class PaymentService:
    """Service for payment-related operations"""
    
    @staticmethod
    def generate_transaction_id() -> str:
        """Generate a unique transaction ID"""
        # Format: TXN-XXXXXXXX (8 random alphanumeric characters)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"TXN-{random_part}"
    
    @staticmethod
    def process_payment_at_system(order_id: int) -> Payment:
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
        
        # Check if order has been finalized (has payment_method set)
        if not order.payment_method:
            raise ValueError("Order has not been finalized. Cannot process payment.")
        
        # Check if payment method is correct
        if order.payment_method != 'card_at_system':
            raise ValueError(f"Order payment method is {order.payment_method}, cannot process system payment")
        
        if order.payment_status != OrderPaymentStatus.PENDING:
            raise ValueError(f"Order payment status is {order.payment_status.value}, cannot process payment")
        
        # Simulate payment processing
        # In a real system, this would call an external payment processor
        transaction_id = PaymentService.generate_transaction_id()
        
        # For now, we'll simulate successful payment
        payment = Payment(
            order_id=order_id,
            amount=order.total,
            payment_method=PaymentMethod.CARD_AT_SYSTEM,
            status=PaymentStatus.APPROVED,
            transaction_id=transaction_id,
            processed_at=datetime.utcnow()
        )
        
        db.session.add(payment)
        
        # Update order status
        order.payment_status = OrderPaymentStatus.PAID
        order.status = OrderStatus.PENDING  # Ready for kitchen
        order.updated_at = datetime.utcnow()
        
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
        
        if order.payment_status != OrderPaymentStatus.PENDING_COUNTER:
            raise ValueError(f"Order payment status is {order.payment_status.value}, cannot process counter payment")
        
        # Determine payment method enum
        if payment_method == 'cash_at_counter':
            method = PaymentMethod.CASH_AT_COUNTER
        elif payment_method == 'card_at_counter':
            method = PaymentMethod.CARD_AT_COUNTER
        else:
            raise ValueError(f"Invalid payment method: {payment_method}")
        
        # Generate transaction ID
        transaction_id = PaymentService.generate_transaction_id()
        
        # Create payment record
        payment = Payment(
            order_id=order_id,
            amount=order.total,
            payment_method=method,
            status=PaymentStatus.APPROVED,
            transaction_id=transaction_id,
            processed_at=datetime.utcnow()
        )
        
        db.session.add(payment)
        
        # Update order status
        order.payment_status = OrderPaymentStatus.PAID
        order.status = OrderStatus.PENDING  # Ready for kitchen
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        return payment
    
    @staticmethod
    def get_payment_by_order_id(order_id: int) -> Optional[Payment]:
        """Get payment record for an order"""
        return Payment.query.filter_by(order_id=order_id).first()

