"""
Test UC4: Add Item to Order
"""
import pytest
from tests.conftest import app, client, sample_menu_items
from database import db
from models.order import Order

class TestUC4AddItemToOrder:
    """Test cases for UC4: Add Item to Order"""
    
    def test_create_new_order(self, client):
        """
        UC4: Test creating a new order
        """
        response = client.post('/api/orders')
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'order' in data
        
        order = data['order']
        assert 'id' in order
        assert 'order_number' in order
        assert order['order_number'].startswith('ORD-')
        assert order['subtotal'] == 0.0
        assert order['tax'] == 0.0
        assert order['total'] == 0.0
        assert order['status'] == 'Pending'
    
    def test_add_item_to_order(self, client, sample_menu_items):
        """
        UC4: Test adding an item to an order
        """
        # Create order
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        menu_item_id = sample_menu_items[0].id
        
        # Add item to order
        response = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': menu_item_id,
                'quantity': 2,
                'customizations': {
                    'size': 'large'
                }
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'order_item' in data
        assert 'order' in data
        
        order_item = data['order_item']
        assert order_item['menu_item_id'] == menu_item_id
        assert order_item['quantity'] == 2
        assert order_item['unit_price'] == 9.99  # 8.99 + 1.00 for large
        assert order_item['item_total'] == 19.98  # 9.99 * 2
        
        # Check order totals updated
        order = data['order']
        assert order['subtotal'] == 19.98
        assert order['tax'] > 0  # Tax should be calculated
        assert order['total'] > order['subtotal']  # Total should include tax
    
    def test_add_item_to_order_invalid_order(self, client, sample_menu_items):
        """Test adding item to non-existent order"""
        menu_item_id = sample_menu_items[0].id
        
        response = client.post(
            '/api/orders/999/items',
            json={
                'menu_item_id': menu_item_id,
                'quantity': 1
            }
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_add_item_to_order_invalid_menu_item(self, client):
        """Test adding non-existent item to order"""
        # Create order
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        response = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': 999,
                'quantity': 1
            }
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_add_item_to_order_missing_fields(self, client):
        """Test adding item with missing required fields"""
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        response = client.post(
            f'/api/orders/{order_id}/items',
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_add_multiple_items_to_order(self, client, sample_menu_items):
        """Test adding multiple different items to an order"""
        # Create order
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        # Add first item
        response1 = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        assert response1.status_code == 201
        
        # Add second item
        response2 = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[1].id,
                'quantity': 2
            }
        )
        assert response2.status_code == 201
        
        # Check order totals
        order_data = response2.get_json()['order']
        assert order_data['subtotal'] == 8.99 + (3.99 * 2)  # Burger + 2 Fries
        assert order_data['tax'] > 0
        assert order_data['total'] == order_data['subtotal'] + order_data['tax']

