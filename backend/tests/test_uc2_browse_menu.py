"""
Test UC2: Browse Menu
"""
import pytest
from tests.conftest import app, client, sample_menu_items

class TestUC2BrowseMenu:
    """Test cases for UC2: Browse Menu"""
    
    def test_get_categories(self, client, sample_menu_items):
        """
        UC2: Test getting all menu categories
        """
        response = client.get('/api/menu/categories')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'categories' in data
        assert isinstance(data['categories'], list)
        assert 'Burgers' in data['categories']
        assert 'Sides' in data['categories']
        assert 'Drinks' in data['categories']
    
    def test_get_all_menu_items(self, client, sample_menu_items):
        """
        UC2: Test getting all menu items
        """
        response = client.get('/api/menu/items')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'items' in data
        assert len(data['items']) == 3
        
        # Check item structure
        item = data['items'][0]
        assert 'id' in item
        assert 'name' in item
        assert 'price' in item
        assert 'category' in item
        assert 'image_url' in item
    
    def test_get_menu_items_by_category(self, client, sample_menu_items):
        """
        UC2: Test getting menu items filtered by category
        """
        response = client.get('/api/menu/items?category=Burgers')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert 'items' in data
        assert len(data['items']) == 1
        assert data['items'][0]['category'] == 'Burgers'
        assert data['items'][0]['name'] == 'Classic Burger'
    
    def test_get_menu_items_by_category_sides(self, client, sample_menu_items):
        """Test getting Sides category items"""
        response = client.get('/api/menu/items?category=Sides')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert len(data['items']) == 1
        assert data['items'][0]['category'] == 'Sides'
    
    def test_get_menu_items_by_category_drinks(self, client, sample_menu_items):
        """Test getting Drinks category items"""
        response = client.get('/api/menu/items?category=Drinks')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'success'
        assert len(data['items']) == 1
        assert data['items'][0]['category'] == 'Drinks'

