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
        if not data:
            return jsonify({
                'error': 'Request body is required',
                'status': 'error'
            }), 400
        
        menu_item_id = data.get('menu_item_id')
        quantity = data.get('quantity', 1)
        customizations = data.get('customizations', {})
        
        if not menu_item_id:
            return jsonify({
                'error': 'menu_item_id is required',
                'status': 'error'
            }), 400
        
        if quantity <= 0:
            return jsonify({
                'error': 'quantity must be greater than 0',
                'status': 'error'
            }), 400
        
        order_item = OrderService.add_item_to_order(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            customizations=customizations
        )
        
        order = OrderService.get_order_by_id(order_id)
        
        return jsonify({
            'order_item': order_item.to_dict(),
            'order': order.to_dict(),
            'status': 'success'
        }), 201
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
        
        if not order:
            return jsonify({
                'error': 'Order not found',
                'status': 'error'
            }), 404
        
        return jsonify({
            'order': order.to_dict(),
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@order_bp.route('/<int:order_id>/items/<int:item_id>', methods=['PUT'])
def update_order_item(order_id, item_id):
    """
    UC5: Review and Edit Current Order
    Update quantity of an order item
    Body: { "quantity": 2 }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Request body is required',
                'status': 'error'
            }), 400
        
        quantity = data.get('quantity')
        if quantity is None:
            return jsonify({
                'error': 'quantity is required',
                'status': 'error'
            }), 400
        
        order_item = OrderService.update_order_item_quantity(item_id, quantity)
        
        if order_item is None:
            # Item was removed
            order = OrderService.get_order_by_id(order_id)
            return jsonify({
                'message': 'Item removed from order',
                'order': order.to_dict(),
                'status': 'success'
            }), 200
        
        order = OrderService.get_order_by_id(order_id)
        
        return jsonify({
            'order_item': order_item.to_dict(),
            'order': order.to_dict(),
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
        OrderService.remove_item_from_order(item_id)
        
        order = OrderService.get_order_by_id(order_id)
        
        return jsonify({
            'message': 'Item removed from order',
            'order': order.to_dict(),
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

# UC6: Confirm Order and Proceed to Payment
@order_bp.route('/<int:order_id>/finalize', methods=['POST'])
def finalize_order(order_id):
    """
    UC6: Confirm Order and Proceed to Payment
    Finalize order and set payment method
    Body: { "payment_method": "card_at_system" | "cash_at_counter" | "card_at_counter" }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Request body is required',
                'status': 'error'
            }), 400
        
        payment_method = data.get('payment_method')
        if not payment_method:
            return jsonify({
                'error': 'payment_method is required',
                'status': 'error'
            }), 400
        
        valid_methods = ['card_at_system', 'cash_at_counter', 'card_at_counter']
        if payment_method not in valid_methods:
            return jsonify({
                'error': f'payment_method must be one of: {", ".join(valid_methods)}',
                'status': 'error'
            }), 400
        
        order = OrderService.finalize_order_for_payment(order_id, payment_method)
        
        return jsonify({
            'order': order.to_dict(),
            'message': 'Order finalized. Proceed to payment.',
            'status': 'success'
        }), 200
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400
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
            'order': order.to_dict(),
            'status': 'success'
        }), 201
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@order_bp.route('/number/<order_number>', methods=['GET'])
def get_order_by_number(order_number):
    """
    Get order by order number
    """
    try:
        order = OrderService.get_order_by_number(order_number)
        
        if not order:
            return jsonify({
                'error': 'Order not found',
                'status': 'error'
            }), 404
        
        return jsonify({
            'order': order.to_dict(),
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

