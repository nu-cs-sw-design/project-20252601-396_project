"""
Order API routes - UC4, UC5, UC6
"""
from flask import Blueprint, jsonify, request
from services.order_service import OrderService
from typing import Dict

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')

# UC4: Add Item to Order
@order_bp.route('/<int:order_id>/items', methods=['POST'])
def add_item_to_order(order_id):
    """
    UC4: Add Item to Order
    Body: {
        "menu_item_id": 1,
        "quantity": 2,
        "customizations": {...}
    }
    """
    try:
        data = request.get_json()
        
        menu_item_id = data.get('menu_item_id')
        quantity = data.get('quantity')
        customizations = data.get('customizations')
        
        
        if quantity <= 0:
            return jsonify({
                'error': 'quantity must be greater than 0',
                'status': 'error'
            }), 400
        
        order = OrderService.add_item_to_order(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            customizations=customizations
        )
        
        return jsonify({
            'message': 'Item added to order',
            'data':order.to_dict(),
            'status': 'success'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
                
        

# UC5: Review and Edit Current Order
@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    UC5: Review and Edit Current Order
    Get order details including all items
    """
    try:
        order = OrderService.get_order_by_id(order_id)
        
        return jsonify({
            'data': order.to_dict(),
            'status': 'success'
        }), 200
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@order_bp.route('/<int:order_id>/items', methods=['PUT'])
def update_order_item(order_id):
    """
    UC5: Review and Edit Current Order
    Update quantity of an order item
    Body: {
        "menu_item_id": 1,
        "quantity": 3,
        "customizations": "please add more cheese"
    }
    """
    try:
        data = request.get_json()
        menu_item_id = int(data.get('menu_item_id'))
        quantity = int(data.get('quantity'))
        customizations = data.get('customizations')
        
        order = OrderService.edit_item_on_order(order_id, menu_item_id, quantity, customizations)
        
        return jsonify({
            'data': order.to_dict(),
            'status': 'success'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@order_bp.route('/<int:order_id>/items/<int:item_id>', methods=['DELETE'])
def remove_order_item(order_id, item_id):
    """
    UC5: Review and Edit Current Order
    Remove an item from the order
    """
    try:
        order = OrderService.remove_item_from_order(order_id, item_id)
        return jsonify({
            'message': 'Item removed from order',
            'status': 'success',
            'data': order.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# Create new order
@order_bp.route('', methods=['POST'])
def create_order():
    """
    Create a new empty order
    """
    try:
        order = OrderService.create_order()
        return jsonify({
            'data': order.to_dict(),
            'status': 'success'
        }), 201
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# confirm order
@order_bp.route('<int:order_id>/confirm', methods=['PUT'])
def confirm_order(order_id:int):
    """
    Create a new empty order
    """
    try:
        order = OrderService.confirmOrder(order_id)
        return jsonify({
            'message': 'order confirmed.',
            'data': order.to_dict(),
            'status': 'success'
        }), 200
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
        
@order_bp.route('/counter-confirmed', methods=['GET'])
def get_counter_confirmed_orders() -> list[Dict]:
    """Get all unpaid orders (for cashier)"""
    try:
        orders = OrderService.get_counter_confirmed_orders()
        orders_data = [order.to_dict() for order in orders]
        return jsonify({
            'data': orders_data,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500