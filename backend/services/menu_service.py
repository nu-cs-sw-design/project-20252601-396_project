"""
Menu Service - Business logic for menu operations
"""
from database import db
from models.menu_item import MenuItem
from typing import List, Optional, Dict

class MenuService:
    """Service for menu-related operations"""
    
    @staticmethod
    def get_all_categories() -> List[str]:
        """Get all unique menu categories"""
        categories = db.session.query(MenuItem.category).distinct().all()
        return [cat[0] for cat in categories if cat[0]]
    
    @staticmethod
    def get_menu_items_by_category(category: str) -> List[MenuItem]:
        """Get all menu items in a specific category"""
        return MenuItem.query.filter_by(
            category=category,
            is_available=True
        ).all()
    
    @staticmethod
    def get_menu_item_by_id(item_id: int) -> Optional[MenuItem]:
        """Get a menu item by ID"""
        return MenuItem.query.get(item_id)
    
    @staticmethod
    def get_all_menu_items() -> List[MenuItem]:
        """Get all available menu items"""
        return MenuItem.query.filter_by(is_available=True).all()
    
    @staticmethod
    def calculate_customized_price(base_price: float, customizations: Dict) -> float:
        """
        Calculate the price of an item with customizations
        
        Args:
            base_price: Base price of the menu item
            customizations: Dictionary of customization options and values
            
        Returns:
            Final price after customizations
        """
        # Stub implementation - can be expanded based on customization rules
        price = base_price
        
        # Example: Add price for size upgrades
        if customizations.get('size') == 'large':
            price += 1.0
        elif customizations.get('size') == 'medium':
            price += 0.5
        
        # Example: Add price for extra toppings
        if customizations.get('extra_toppings'):
            price += len(customizations.get('extra_toppings', [])) * 0.5
        
        return round(price, 2)

