"""
Test UC7: Complete Payment at System
"""
import pytest
from tests.conftest import app, client, sample_menu_items
from database import db
from models.order import Order, OrderStatus, PaymentStatus as OrderPaymentStatus

class TestUC7Payment:
    """Test cases for UC7: Complete Payment at System"""
    
    def test_process_payment_at_system(self, client, sample_menu_items):
        """
        UC7: Test processing payment at system (card payment)
        """
        # Create order, add item, and finalize
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        
        # Process payment
        response = client.post(
            '/api/payments/process-system',
            json={'order_id': order_id}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'payment' in data
        assert 'order' in data
        assert 'order_number' in data
        
        payment = data['payment']
        assert payment['status'] == 'Approved'
        assert payment['payment_method'] == 'card_at_system'
        assert payment['amount'] > 0
        assert 'transaction_id' in payment
        assert payment['transaction_id'].startswith('TXN-')
        
        order = data['order']
        assert order['payment_status'] == 'Paid'
        assert order['status'] == 'Pending'  # Ready for kitchen
    
    def test_process_payment_missing_order_id(self, client):
        """Test processing payment without order_id"""
        response = client.post(
            '/api/payments/process-system',
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_process_payment_invalid_order(self, client):
        """Test processing payment for non-existent order"""
        response = client.post(
            '/api/payments/process-system',
            json={'order_id': 999}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_process_payment_wrong_status(self, client, sample_menu_items):
        """Test processing payment for order with wrong payment status"""
        # Create order and add item (but don't finalize)
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        # Try to process payment without finalizing
        response = client.post(
            '/api/payments/process-system',
            json={'order_id': order_id}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_process_payment_creates_transaction_id(self, client, sample_menu_items):
        """Test that payment creates unique transaction ID"""
        # Create and finalize order
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        
        # Process payment
        response = client.post(
            '/api/payments/process-system',
            json={'order_id': order_id}
        )
        
        assert response.status_code == 200
        payment = response.get_json()['payment']
        
        assert payment['transaction_id'] is not None
        assert len(payment['transaction_id']) > 0
        assert payment['processed_at'] is not None
    
    def test_payment_updates_order_status(self, client, sample_menu_items):
        """Test that payment updates order status correctly"""
        # Create and finalize order
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        
        # Verify order status before payment
        get_order = client.get(f'/api/orders/{order_id}')
        assert get_order.get_json()['order']['payment_status'] == 'Pending'
        
        # Process payment
        response = client.post(
            '/api/payments/process-system',
            json={'order_id': order_id}
        )
        
        assert response.status_code == 200
        
        # Verify order status after payment
        get_order_after = client.get(f'/api/orders/{order_id}')
        order_after = get_order_after.get_json()['order']
        assert order_after['payment_status'] == 'Paid'
        assert order_after['status'] == 'Pending'  # Ready for kitchen queue

