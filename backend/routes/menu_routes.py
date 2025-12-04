"""
Menu API routes - UC1, UC2, UC3
"""
from flask import Blueprint, jsonify, request
from services.menu_service import MenuService
from typing import Dict

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menu')


# UC2: Browse Menu - Get categories
@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    UC2: Browse Menu - Get all menu categories
    """
    try:
        categories = MenuService.getMenuCategories()
        return jsonify({
            'data': categories,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@menu_bp.route('/items-by-category/<string:category>', methods=['GET'])
def get_menu_items(category: str):
    """
    UC2: Browse Menu - Get menu items
    Query params:
        - category: Filter by category (optional)
    """
    try:        
        
        items = MenuService.getMenuItemsByCategory(category)
        
        return jsonify({
            'data': [item.to_dict() for item in items],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
        
@menu_bp.route('/items', methods=['GET'])
def get_all_menu_items():
    
    try:        
        items = MenuService.getAllMenuItems()
        return jsonify({
            'data': [item.to_dict() for item in items],
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
        item = MenuService.getItemDetails(item_id)
        return jsonify({
            'data': item.to_dict(),
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@menu_bp.route('/items', methods=['POST'])
def add_new_menu_item():
    data = request.get_json()
    try:
        name = data.get('name')
        price = data.get('price')
        category = data.get('category')
        description = data.get('description', '')

        if not all([name, price, category]):
            return jsonify({
                'error': 'Missing required fields',
                'status': 'error'
            }), 400

        item = MenuService.addNewMenuItem(name, price, category, description)

        return jsonify({
            'data': item.to_dict(),
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
        
@menu_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id: int):
    try:
        data = request.get_json()
        price = data.get('price')
        category = data.get('category')
        description = data.get('description', '')
        MenuService.updateExistingMenuItem(item_id, price, category, description)

        return jsonify({
            'status': 'success'
        }), 200

    except ValueError as ve:
        return jsonify({
            'error': str(ve),
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500