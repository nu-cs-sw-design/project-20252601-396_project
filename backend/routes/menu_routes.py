"""
Menu API routes - UC1, UC2, UC3
"""
from flask import Blueprint, jsonify, request
from services.menu_service import MenuService
from typing import Dict

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menu')

# UC1: Start the System - Welcome message and main menu
@menu_bp.route('/welcome', methods=['GET'])
def get_welcome():
    """
    UC1: Start the System
    Returns welcome message and indicates system is ready
    """
    return jsonify({
        'message': 'Welcome to Fast Food Ordering System',
        'status': 'ready',
        'main_menu_available': True
    }), 200

# UC2: Browse Menu - Get categories and menu items
@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    UC2: Browse Menu - Get all menu categories
    """
    try:
        categories = MenuService.get_all_categories()
        return jsonify({
            'categories': categories,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@menu_bp.route('/items', methods=['GET'])
def get_menu_items():
    """
    UC2: Browse Menu - Get menu items
    Query params:
        - category: Filter by category (optional)
    """
    try:
        category = request.args.get('category')
        
        if category:
            items = MenuService.get_menu_items_by_category(category)
        else:
            items = MenuService.get_all_menu_items()
        
        return jsonify({
            'items': [item.to_dict() for item in items],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@menu_bp.route('/items/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """
    UC3: View Item Details and Customize Item
    Get detailed information about a menu item including customization options
    """
    try:
        item = MenuService.get_menu_item_by_id(item_id)
        
        if not item:
            return jsonify({
                'error': 'Menu item not found',
                'status': 'error'
            }), 404
        
        return jsonify({
            'item': item.to_dict(),
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@menu_bp.route('/items/<int:item_id>/calculate-price', methods=['POST'])
def calculate_customized_price(item_id):
    """
    UC3: View Item Details and Customize Item
    Calculate price with customizations
    Body: { "customizations": {...} }
    """
    try:
        item = MenuService.get_menu_item_by_id(item_id)
        if not item:
            return jsonify({
                'error': 'Menu item not found',
                'status': 'error'
            }), 404
        
        data = request.get_json() or {}
        customizations = data.get('customizations', {})
        
        base_price = item.price
        customized_price = MenuService.calculate_customized_price(base_price, customizations)
        
        return jsonify({
            'base_price': base_price,
            'customized_price': customized_price,
            'customizations': customizations,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

