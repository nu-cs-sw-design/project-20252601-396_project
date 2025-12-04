from flask import Blueprint, request, jsonify
from services.kitchen_service import KitchenService

kitchen_bp = Blueprint('kitchen', __name__, url_prefix='/api/kitchen')

@kitchen_bp.route('/order-queue', methods=['GET'])
def get_pending_orders():
    try:
        orders = KitchenService.get_order_queue()
        orders_data = [order.to_dict() for order in orders]  # Assuming Order model has a to_dict method
        return jsonify({'data': orders_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@kitchen_bp.route('/update-order-status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id: int):
    try:
        data = request.get_json()
        status = data.get('status')
        
        KitchenService.update_order_status(order_id, status)
        
        return jsonify({'message': 'Order status updated successfully'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@kitchen_bp.route('/cancel-order', methods=['POST'])
def cancel_order():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        KitchenService.cancel_order(order_id)
        
        return jsonify({'message': 'Order cancelled successfully'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    