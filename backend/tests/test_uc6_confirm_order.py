"""
Test UC6: Confirm Order and Proceed to Payment
"""
import pytest
from tests.conftest import app, client, sample_menu_items

class TestUC6ConfirmOrder:
    """Test cases for UC6: Confirm Order and Proceed to Payment"""
    
    def test_finalize_order_card_at_system(self, client, sample_menu_items):
        """
        UC6: Test finalizing order with card at system payment method
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        # Finalize order
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'order' in data
        
        order = data['order']
        assert order['payment_method'] == 'card_at_system'
        assert order['payment_status'] == 'Pending'
        assert order['total'] > 0
        assert 'tax' in order
        assert order['tax'] > 0
    
    def test_finalize_order_cash_at_counter(self, client, sample_menu_items):
        """
        UC6: Test finalizing order with cash at counter payment method
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        # Finalize order
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'cash_at_counter'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        order = data['order']
        assert order['payment_method'] == 'cash_at_counter'
        assert order['payment_status'] == 'Pending Payment at Counter'
    
    def test_finalize_order_card_at_counter(self, client, sample_menu_items):
        """
        UC6: Test finalizing order with card at counter payment method
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        # Finalize order
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_counter'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        order = data['order']
        assert order['payment_method'] == 'card_at_counter'
        assert order['payment_status'] == 'Pending Payment at Counter'
    
    def test_finalize_order_missing_payment_method(self, client, sample_menu_items):
        """Test finalizing order without payment method"""
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_finalize_order_invalid_payment_method(self, client, sample_menu_items):
        """Test finalizing order with invalid payment method"""
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'invalid_method'}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_finalize_order_without_items(self, client):
        """Test finalizing empty order (should fail)"""
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        assert 'no items' in data['error'].lower() or 'cannot finalize' in data['error'].lower()
    
    def test_finalize_order_calculates_tax(self, client, sample_menu_items):
        """Test that finalizing order correctly calculates tax"""
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        
        response = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        
        assert response.status_code == 200
        order = response.get_json()['order']
        
        # Tax should be 8% of subtotal
        expected_tax = round(8.99 * 0.08, 2)
        assert abs(order['tax'] - expected_tax) < 0.01
        assert abs(order['total'] - (order['subtotal'] + order['tax'])) < 0.01

