"""
API Routes
"""
from flask import Blueprint
from routes.main import main_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from routes.payment_routes import payment_bp

__all__ = ['main_bp', 'menu_bp', 'order_bp', 'payment_bp']

