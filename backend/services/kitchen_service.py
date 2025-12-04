"""
Menu Service - Business logic for menu operations
"""
from database import db
from models.order import Order, OrderStatus
from services.order_service import OrderService
from typing import List

class KitchenService:
    """Service for menu-related operations"""
    @staticmethod
    def get_order_queue() -> List[Order]:
        """Get all orders that are in the queue (PAID and PREPARING)"""
        return Order.query.filter(Order.status.in_([OrderStatus.PAID, OrderStatus.PREPARING])).all()
    
    def update_order_status(order_id: int, status: str) -> None:
        """Update the status of an order"""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        try:
            new_status = OrderStatus(status)
        except ValueError:
            raise ValueError(f"Invalid order status: {status}")
        
        order.status = new_status
        db.session.commit()
        
    def cancel_order(order_id: int) -> None:
        """Cancel an order"""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        order.status = OrderStatus.CANCELLED
        db.session.commit()
