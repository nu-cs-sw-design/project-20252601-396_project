"""
Test UC1: Start the System
"""
import pytest
from tests.conftest import app, client

class TestUC1StartSystem:
    """Test cases for UC1: Start the System"""
    
    def test_health_check(self, client):
        """Test that the health check endpoint works"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['status'] == 'ok'
        assert 'Fast Food Ordering System API' in data['message']

