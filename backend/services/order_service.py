"""
Order Service - Business logic for order operations
"""
from database import db
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.menu_item import MenuItem
from services.menu_service import MenuService
from typing import List, Optional, Dict
from datetime import datetime
import random
import string

class OrderService:
    """Service for order-related operations"""
    TAX_RATE = 0.08
    @staticmethod
    def create_order() -> Order:
        """Create a new empty order"""
        order = Order(
            status=OrderStatus.PENDING,
            total=0.0,
        )
        db.session.add(order)
        db.session.commit()
        return order
    
    @staticmethod
    def get_order_by_id(order_id: int):
        """Get an order by ID"""
        order = Order.query.get(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")
        return order
    
    @staticmethod
    def add_item_to_order(order_id: int, menu_item_id: int, quantity: int, 
                         customizations: string = None)-> Order:
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
        
        menu_item = MenuService.getItemDetails(menu_item_id)
        # Create order item
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            unit_price=menu_item.price,
            customizations=customizations
        )
        
        db.session.add(order_item)
        
        # Update order totals
        OrderService._update_order_totals(order_id)
        
        db.session.commit()
        return order
    
    @staticmethod
    def edit_item_on_order(orderID: int, menu_item_id:int, quantity: int, customizations: string):
        """
        Update the quantity of an order item
        
        Args:
            order_item_id: ID of the order item
            quantity: New quantity
            
        Returns:
            Updated OrderItem
        """
        order = OrderService.get_order_by_id(orderID)
        
        if not order:
            raise ValueError(f"Order of id {orderID} not found")
        order_item = None
        for item in order.order_items:
            if item.menu_item.id == menu_item_id:
                order_item = item
        if not order_item:
            raise ValueError(f"Order item {menu_item_id} not found on order {orderID}")
        
        if quantity <= 0:
            db.session.delete(order_item)
            db.session.commit()
            OrderService._update_order_totals(orderID)
            return order
        
        order_item.quantity = quantity
        order_item.customizations = customizations     
        db.session.commit()
        OrderService._update_order_totals(order_item.order_id)
        return order
    
    @staticmethod
    def remove_item_from_order(orderID: int, menu_item_id: int) -> None:
        """Remove an item from an order"""
        order = OrderService.get_order_by_id(orderID)
        if not order:
            raise ValueError(f"Order of id {orderID} not found")
        order_item = None
        for item in order.order_items:
            if item.menu_item.id == menu_item_id:
                order_item = item
        if not order_item:
            raise ValueError(f"Order item {menu_item_id} not found on order {orderID}")
        
        db.session.delete(order_item)
        db.session.commit()
        
        # Update order totals
        OrderService._update_order_totals(orderID)
        return order
    
    @staticmethod
    def _update_order_totals(order_id: int) -> None:
        """Recalculate and update order subtotal, tax, and total"""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")
        
        # Calculate subtotal from all order items
        order_items = order.order_items
        # Update order
        subtotal = sum(item.unit_price * item.quantity for item in order_items)
        order.total = round(subtotal * (1+OrderService.TAX_RATE), 2)
        db.session.commit()

    @staticmethod
    def reviewOrder(order_id: int) -> Order:
        """Get order details including all items"""
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")
        return order
    
    @staticmethod
    def confirmOrder(order_id:int):
        order = OrderService.get_order_by_id(order_id)
        order.status = OrderStatus.CONFIRMED
        db.session.commit()
        return order
    
    @staticmethod
    def get_counter_confirmed_orders() -> list[Order]:
        """Get all orders that are unpaid (CONFIRMED)"""
        return Order.query.filter(Order.status.in_([OrderStatus.CONFIRMED])).all()