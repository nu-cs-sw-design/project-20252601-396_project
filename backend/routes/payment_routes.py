"""
Payment API routes - UC7
"""
from flask import Blueprint, jsonify, request
from services.payment_service import PaymentService
from services.order_service import OrderService

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payments')

# UC7: Complete Payment at System
@payment_bp.route('/process-system', methods=['POST'])
def process_payment_at_system():
    """
    UC7: Complete Payment at System
    Process card payment at the kiosk system
    Body: { "order_id": 1 }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Request body is required',
                'status': 'error'
            }), 400
        
        
        order_id = data.get('order_id')
        card_info = data.get('card_info')
        
        payment = PaymentService.process_payment_at_system(order_id, card_info)
        
        return jsonify({
            'data': payment.to_dict(),
            'message': 'Payment approved. Order sent to kitchen.',
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

@payment_bp.route('/process-counter', methods=['POST'])
def process_payment_at_counter():
    """
    UC9: Complete Payment at Counter (for cashier)
    Process payment at the counter (cash or card)
    Body: {
        "order_id": 1,
        "payment_method": "cash_at_counter" | "card_at_counter"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Request body is required',
                'status': 'error'
            }), 400
        
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')
        payment = PaymentService.process_payment_at_counter(order_id, payment_method)
        
        return jsonify({
            'data': payment.to_dict(),
            'message': 'Payment processed successfully. Order sent to kitchen.',
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

