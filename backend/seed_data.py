"""
Seed script to populate initial menu data
Run this script to add sample menu items to the database
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database import db
from models.menu_item import MenuItem

def seed_menu_items():
    """Seed the database with sample menu items"""
    app = create_app()
    
    with app.app_context():
        # Check if menu items already exist
        if MenuItem.query.first():
            print("Menu items already exist. Skipping seed.")
            return
        
        # Sample menu items
        menu_items = [
            # Burgers
            MenuItem(
                name="Classic Burger",
                description="Juicy beef patty with lettuce, tomato, and special sauce",
                price=8.99,
                category="Burgers",
                image_url="/images/classic-burger.jpg",
                customization_options={
                    "size": ["regular", "large"],
                    "toppings": ["lettuce", "tomato", "onion", "pickles", "cheese"],
                    "patty": ["beef", "chicken", "veggie"]
                },
                is_available=True
            ),
            MenuItem(
                name="Cheeseburger",
                description="Classic burger with melted cheese",
                price=9.99,
                category="Burgers",
                image_url="/images/cheeseburger.jpg",
                customization_options={
                    "size": ["regular", "large"],
                    "toppings": ["lettuce", "tomato", "onion", "pickles"],
                    "cheese_type": ["cheddar", "swiss", "american"]
                },
                is_available=True
            ),
            MenuItem(
                name="Bacon Burger",
                description="Burger topped with crispy bacon",
                price=10.99,
                category="Burgers",
                image_url="/images/bacon-burger.jpg",
                customization_options={
                    "size": ["regular", "large"],
                    "toppings": ["lettuce", "tomato", "onion", "pickles", "cheese"]
                },
                is_available=True
            ),
            
            # Sides
            MenuItem(
                name="French Fries",
                description="Crispy golden fries",
                price=3.99,
                category="Sides",
                image_url="/images/fries.jpg",
                customization_options={
                    "size": ["small", "medium", "large"]
                },
                is_available=True
            ),
            MenuItem(
                name="Onion Rings",
                description="Crispy battered onion rings",
                price=4.99,
                category="Sides",
                image_url="/images/onion-rings.jpg",
                customization_options={
                    "size": ["small", "medium", "large"]
                },
                is_available=True
            ),
            MenuItem(
                name="Chicken Nuggets",
                description="6 pieces of crispy chicken nuggets",
                price=5.99,
                category="Sides",
                image_url="/images/nuggets.jpg",
                customization_options={
                    "quantity": [6, 10, 20],
                    "sauce": ["bbq", "ranch", "honey_mustard", "sweet_sour"]
                },
                is_available=True
            ),
            
            # Drinks
            MenuItem(
                name="Coca Cola",
                description="Refreshing cola drink",
                price=2.49,
                category="Drinks",
                image_url="/images/coke.jpg",
                customization_options={
                    "size": ["small", "medium", "large"]
                },
                is_available=True
            ),
            MenuItem(
                name="Sprite",
                description="Lemon-lime soda",
                price=2.49,
                category="Drinks",
                image_url="/images/sprite.jpg",
                customization_options={
                    "size": ["small", "medium", "large"]
                },
                is_available=True
            ),
            MenuItem(
                name="Orange Juice",
                description="Fresh squeezed orange juice",
                price=3.49,
                category="Drinks",
                image_url="/images/orange-juice.jpg",
                customization_options={
                    "size": ["small", "medium", "large"]
                },
                is_available=True
            ),
        ]
        
        # Add all items to database
        for item in menu_items:
            db.session.add(item)
        
        db.session.commit()
        print(f"Successfully seeded {len(menu_items)} menu items!")

if __name__ == '__main__':
    seed_menu_items()

