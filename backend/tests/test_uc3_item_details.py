"""
Test UC3: View Item Details and Customize Item
"""
import pytest
from tests.conftest import app, client, sample_menu_items

class TestUC3ItemDetails:
    """Test cases for UC3: View Item Details and Customize Item"""
    
    def test_get_item_details(self, client, sample_menu_items):
        """
        UC3: Test getting detailed information about a menu item
        """
        item_id = sample_menu_items[0].id
        response = client.get(f'/api/menu/items/{item_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'item' in data
        
        item = data['item']
        assert item['id'] == item_id
        assert item['name'] == 'Classic Burger'
        assert item['description'] == 'Juicy beef patty'
        assert item['price'] == 8.99
        assert item['category'] == 'Burgers'
        assert 'customization_options' in item
        assert 'size' in item['customization_options']
        assert 'toppings' in item['customization_options']
    
    def test_get_item_details_not_found(self, client):
        """Test getting non-existent item"""
        response = client.get('/api/menu/items/999')
        
        assert response.status_code == 404
        data = response.get_json()
        
        assert data['status'] == 'error'
        assert 'not found' in data['error'].lower()
    
    def test_calculate_price_with_customizations(self, client, sample_menu_items):
        """
        UC3: Test calculating price with customizations
        """
        item_id = sample_menu_items[0].id
        
        # Test with size customization
        response = client.post(
            f'/api/menu/items/{item_id}/calculate-price',
            json={
                'customizations': {
                    'size': 'large'
                }
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'base_price' in data
        assert 'customized_price' in data
        assert data['base_price'] == 8.99
        # Large size should add $1.00
        assert data['customized_price'] == 9.99
    
    def test_calculate_price_with_multiple_customizations(self, client, sample_menu_items):
        """Test calculating price with multiple customizations"""
        item_id = sample_menu_items[0].id
        
        response = client.post(
            f'/api/menu/items/{item_id}/calculate-price',
            json={
                'customizations': {
                    'size': 'large',
                    'extra_toppings': ['bacon', 'cheese']
                }
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        # Base: 8.99, Large: +1.00, 2 toppings: +1.00 = 10.99
        assert data['customized_price'] == 10.99
    
    def test_calculate_price_no_customizations(self, client, sample_menu_items):
        """Test calculating price without customizations"""
        item_id = sample_menu_items[0].id
        
        response = client.post(
            f'/api/menu/items/{item_id}/calculate-price',
            json={
                'customizations': {}
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert data['base_price'] == data['customized_price'] == 8.99

