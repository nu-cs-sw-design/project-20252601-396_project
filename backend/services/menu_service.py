"""
Menu Service - Business logic for menu operations
"""
from database import db
from models.menu_item import MenuItem
from typing import List, Optional, Dict

class MenuService:
    """Service for menu-related operations"""

    @staticmethod
    def getMenuCategories() -> List[str]:
        """Get all unique menu categories"""
        categories = db.session.query(MenuItem.category).distinct().all()
        return [c[0] for c in categories if c[0]]
    
    @staticmethod
    def getMenuItemsByCategory(category: str) -> List[MenuItem]:
        """Get all menu items in a specific category"""
        return MenuItem.query.filter_by(
            category=category,
        ).all()
    
    @staticmethod
    def getAllMenuItems() -> List[MenuItem]:
        """Get all menu items"""
        return MenuItem.query.all()
    
    @staticmethod
    def getItemDetails(item_id: int) -> MenuItem:
        """Get a menu item by ID"""
        item = MenuItem.query.get(item_id)
        if not item:
            raise ValueError(f"Menu item with id {item_id} not found.")
        return item
    
    @staticmethod
    def addNewMenuItem(name: str, price: float, category: str, description: str) -> MenuItem:
        """Add a new menu item"""
        item = MenuItem(
            name=name.strip(),
            price=price,
            category=category.strip(),
            description=description.strip() if description else "",
        )

        db.session.add(item)
        db.session.commit()

        return item

    
    @staticmethod
    def updateExistingMenuItem(item_id: int, price: float, category: str, description: str) -> None:
        item: Optional[MenuItem] = MenuItem.query.get(item_id)
        if item is None:
            raise ValueError(f"Menu item with id {item_id} not found.")

        item.price = price
        if category:
            item.category = category.strip()
        if description:
            item.description = description.strip()

        db.session.commit()





