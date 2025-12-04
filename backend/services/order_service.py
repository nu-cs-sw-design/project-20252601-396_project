"""
Order Service - Business logic for order operations
"""
from database import db
from models.order import Order, OrderStatus, PaymentStatus
from models.order_item import OrderItem
from models.menu_item import MenuItem
from services.menu_service import MenuService
from typing import List, Optional, Dict
from datetime import datetime
import random
import string

class OrderService:
    """Service for order-related operations"""
    
    TAX_RATE = 0.08  # 8% tax rate
    
    @staticmethod
    def generate_order_number() -> str:
        """Generate a unique order number"""
        # Format: ORD-XXXXXX (6 random alphanumeric characters)
        while True:
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            order_number = f"ORD-{random_part}"
            
            # Check if order number already exists
            existing = Order.query.filter_by(order_number=order_number).first()
            if not existing:
                return order_number
    
    @staticmethod
    def create_order() -> Order:
        """Create a new empty order"""
        order = Order(
            order_number=OrderService.generate_order_number(),
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            subtotal=0.0,
            tax=0.0,
            total=0.0
        )
        db.session.add(order)
        db.session.commit()
        return order
    
    @staticmethod
    def get_order_by_id(order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        return Order.query.get(order_id)
    
    @staticmethod
    def get_order_by_number(order_number: str) -> Optional[Order]:
        """Get an order by order number"""
        return Order.query.filter_by(order_number=order_number).first()
    
    @staticmethod
    def add_item_to_order(order_id: int, menu_item_id: int, quantity: int, 
                         customizations: Dict = None) -> OrderItem:
        """
        Add an item to an order
        
        Args:
            order_id: ID of the order
            menu_item_id: ID of the menu item
            quantity: Quantity of the item
            customizations: Dictionary of customization options
            
        Returns:
            Created OrderItem
        """
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        menu_item = MenuService.get_menu_item_by_id(menu_item_id)
        if not menu_item:
            raise ValueError(f"Menu item {menu_item_id} not found")
        
        # Calculate price with customizations
        unit_price = MenuService.calculate_customized_price(
            menu_item.price,
            customizations or {}
        )
        
        item_total = unit_price * quantity
        
        # Create order item
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            unit_price=unit_price,
            customizations=customizations or {},
            item_total=item_total
        )
        
        db.session.add(order_item)
        
        # Update order totals
        OrderService._update_order_totals(order_id)
        
        db.session.commit()
        return order_item
    
    @staticmethod
    def update_order_item_quantity(order_item_id: int, quantity: int) -> OrderItem:
        """
        Update the quantity of an order item
        
        Args:
            order_item_id: ID of the order item
            quantity: New quantity
            
        Returns:
            Updated OrderItem
        """
        order_item = OrderItem.query.get(order_item_id)
        if not order_item:
            raise ValueError(f"Order item {order_item_id} not found")
        
        if quantity <= 0:
            # Remove item if quantity is 0 or less
            order_id = order_item.order_id
            db.session.delete(order_item)
            db.session.commit()
            OrderService._update_order_totals(order_id)
            return None
        
        order_item.quantity = quantity
        order_item.item_total = order_item.unit_price * quantity
        
        db.session.commit()
        
        # Update order totals
        OrderService._update_order_totals(order_item.order_id)
        
        return order_item
    
    @staticmethod
    def remove_item_from_order(order_item_id: int) -> None:
        """Remove an item from an order"""
        order_item = OrderItem.query.get(order_item_id)
        if not order_item:
            raise ValueError(f"Order item {order_item_id} not found")
        
        order_id = order_item.order_id
        db.session.delete(order_item)
        db.session.commit()
        
        # Update order totals
        OrderService._update_order_totals(order_id)
    
    @staticmethod
    def get_order_items(order_id: int) -> List[OrderItem]:
        """Get all items in an order"""
        return OrderItem.query.filter_by(order_id=order_id).all()
    
    @staticmethod
    def _update_order_totals(order_id: int) -> None:
        """Recalculate and update order subtotal, tax, and total"""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            return
        
        # Calculate subtotal from all order items
        order_items = OrderService.get_order_items(order_id)
        subtotal = sum(item.item_total for item in order_items)
        
        # Calculate tax
        tax = round(subtotal * OrderService.TAX_RATE, 2)
        
        # Calculate total
        total = round(subtotal + tax, 2)
        
        # Update order
        order.subtotal = subtotal
        order.tax = tax
        order.total = total
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
    
    @staticmethod
    def finalize_order_for_payment(order_id: int, payment_method: str) -> Order:
        """
        Finalize order and prepare for payment
        
        Args:
            order_id: ID of the order
            payment_method: Payment method selected
            
        Returns:
            Updated Order
        """
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if not order.order_items:
            raise ValueError("Cannot finalize order with no items")
        
        order.payment_method = payment_method
        
        if payment_method == 'card_at_system':
            order.payment_status = PaymentStatus.PENDING
        elif payment_method in ['cash_at_counter', 'card_at_counter']:
            order.payment_status = PaymentStatus.PENDING_COUNTER
        
        db.session.commit()
        return order

