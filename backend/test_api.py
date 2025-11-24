#!/usr/bin/env python3
"""
Simple script to test the API endpoints
Run this while app.py is running to test all endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_endpoint(method, url, data=None, description=""):
    """Test an API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{method} {url}")
    print(f"{'='*60}")
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        return response
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Is app.py running?")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    print("\n" + "="*60)
    print("Fast Food Ordering System - API Test Script")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure app.py is running before testing!")
    print("="*60)
    
    # UC1: Start the System
    test_endpoint('GET', f'{BASE_URL}/', description="UC1: Health Check")
    test_endpoint('GET', f'{BASE_URL}/api/menu/welcome', description="UC1: Welcome Message")
    
    # UC2: Browse Menu
    test_endpoint('GET', f'{BASE_URL}/api/menu/categories', description="UC2: Get Categories")
    test_endpoint('GET', f'{BASE_URL}/api/menu/items', description="UC2: Get All Items")
    test_endpoint('GET', f'{BASE_URL}/api/menu/items?category=Burgers', description="UC2: Get Items by Category")
    
    # UC3: View Item Details
    test_endpoint('GET', f'{BASE_URL}/api/menu/items/1', description="UC3: Get Item Details")
    test_endpoint('POST', f'{BASE_URL}/api/menu/items/1/calculate-price', 
                  data={'customizations': {'size': 'large'}}, 
                  description="UC3: Calculate Price with Customizations")
    
    # UC4: Add Item to Order
    order_response = test_endpoint('POST', f'{BASE_URL}/api/orders', description="UC4: Create Order")
    
    if order_response and order_response.status_code == 201:
        order_id = order_response.json()['order']['id']
        test_endpoint('POST', f'{BASE_URL}/api/orders/{order_id}/items',
                     data={'menu_item_id': 1, 'quantity': 2, 'customizations': {'size': 'large'}},
                     description="UC4: Add Item to Order")
        
        # UC5: Review Order
        test_endpoint('GET', f'{BASE_URL}/api/orders/{order_id}', description="UC5: Review Order")
        
        # UC6: Finalize Order
        test_endpoint('POST', f'{BASE_URL}/api/orders/{order_id}/finalize',
                     data={'payment_method': 'card_at_system'},
                     description="UC6: Finalize Order")
        
        # UC7: Process Payment
        test_endpoint('POST', f'{BASE_URL}/api/payments/process-system',
                     data={'order_id': order_id},
                     description="UC7: Process Payment")
    
    print("\n" + "="*60)
    print("API Testing Complete!")
    print("="*60)

if __name__ == '__main__':
    main()

