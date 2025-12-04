"""
Test UC5: Review and Edit Current Order
"""
import pytest
from tests.conftest import app, client, sample_menu_items

class TestUC5ReviewEditOrder:
    """Test cases for UC5: Review and Edit Current Order"""
    
    def test_get_order_details(self, client, sample_menu_items):
        """
        UC5: Test getting order details with items
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 2
            }
        )
        
        # Get order details
        response = client.get(f'/api/orders/{order_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'order' in data
        
        order = data['order']
        assert order['id'] == order_id
        assert 'order_items' in order
        assert len(order['order_items']) == 1
        assert order['order_items'][0]['quantity'] == 2
    
    def test_get_order_not_found(self, client):
        """Test getting non-existent order"""
        response = client.get('/api/orders/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_update_item_quantity(self, client, sample_menu_items):
        """
        UC5: Test updating item quantity in order
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        add_response = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        item_id = add_response.get_json()['order_item']['id']
        
        # Update quantity
        response = client.put(
            f'/api/orders/{order_id}/items/{item_id}',
            json={'quantity': 3}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert data['order_item']['quantity'] == 3
        assert data['order_item']['item_total'] == 8.99 * 3
        
        # Check order totals updated
        order = data['order']
        assert order['subtotal'] == 8.99 * 3
    
    def test_remove_item_by_setting_quantity_zero(self, client, sample_menu_items):
        """
        UC5: Test removing item by setting quantity to 0
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        add_response = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        item_id = add_response.get_json()['order_item']['id']
        
        # Remove item
        response = client.put(
            f'/api/orders/{order_id}/items/{item_id}',
            json={'quantity': 0}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'Item removed' in data['message']
        assert data['order']['subtotal'] == 0.0
    
    def test_remove_item_from_order(self, client, sample_menu_items):
        """
        UC5: Test removing item from order using DELETE
        """
        # Create order and add item
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        add_response = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        item_id = add_response.get_json()['order_item']['id']
        
        # Remove item
        response = client.delete(f'/api/orders/{order_id}/items/{item_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'Item removed' in data['message']
        assert data['order']['subtotal'] == 0.0
    
    def test_edit_order_with_multiple_items(self, client, sample_menu_items):
        """Test editing order that has multiple items"""
        # Create order and add multiple items
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        # Add first item
        add1 = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        item1_id = add1.get_json()['order_item']['id']
        
        # Add second item
        add2 = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[1].id,
                'quantity': 2
            }
        )
        item2_id = add2.get_json()['order_item']['id']
        
        # Update first item quantity
        response = client.put(
            f'/api/orders/{order_id}/items/{item1_id}',
            json={'quantity': 3}
        )
        
        assert response.status_code == 200
        order = response.get_json()['order']
        
        # Check totals include both items
        expected_subtotal = (8.99 * 3) + (3.99 * 2)
        assert abs(order['subtotal'] - expected_subtotal) < 0.01
        
        # Remove second item
        remove_response = client.delete(f'/api/orders/{order_id}/items/{item2_id}')
        assert remove_response.status_code == 200
        
        final_order = remove_response.get_json()['order']
        assert abs(final_order['subtotal'] - (8.99 * 3)) < 0.01

