#!/usr/bin/env python3
"""
Simple script to test the API endpoints
Run this while app.py is running to test all endpoints
"""
import requests
import json
from datetime import datetime
from models.order import OrderStatus

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
    
    # UC2: Browse Menu
    test_endpoint('GET', f'{BASE_URL}/api/menu/categories', description="UC2: Get Categories")
    test_endpoint('GET', f'{BASE_URL}/api/menu/items-by-category/Burgers', description="UC2: Get Items by Category")
    
    # UC3: View Item Details
    test_endpoint('GET', f'{BASE_URL}/api/menu/items/1', description="UC3: Get Item Details")
    
    # UC4: Add Item to Order
    order1_response = test_endpoint('POST', f'{BASE_URL}/api/orders', description="UC4: Create Order")
    order2_response = test_endpoint('POST', f'{BASE_URL}/api/orders', description="UC4: Create Another Order")
    
    if order1_response and order1_response.status_code == 201:
        order_id1 = order1_response.json()['data']['id']
        order_id2 = order2_response.json()['data']['id']
        test_endpoint('POST', f'{BASE_URL}/api/orders/{order_id1}/items',
                     data={'menu_item_id': 1, 'quantity': 2, 'customizations':""},
                     description="UC4: Add Item to Order")
        test_endpoint('POST', f'{BASE_URL}/api/orders/{order_id2}/items',
                     data={'menu_item_id': 2, 'quantity': 1, 'customizations': ""},
                     description="UC4: Add Another Item to Order")
        
        # UC5: Review Order
        test_endpoint('GET', f'{BASE_URL}/api/orders/{order_id1}', description="UC5: Review Order")
        test_endpoint('GET', f'{BASE_URL}/api/orders/{order_id2}', description="UC5: Review Another Order")
        
        # UC6: Finalize Order
        test_endpoint('PUT', f'{BASE_URL}/api/orders/{order_id2}/confirm', description="UC6: Finalize order for Counter Payment")
        
        # UC7: Process Payment at system
        test_endpoint('POST', f'{BASE_URL}/api/payments/process-system',
                     data={'order_id': order_id1, 'card_info': "1724017497183746"},
                     description="UC8: Process Payment at system")
        # UC9/10: Process Payment at counter
        test_endpoint('POST', f'{BASE_URL}/api/payments/process-counter',
                     data={'order_id': order_id2, 'payment_method': 'cash_at_counter'},
                     description="UC9: Process Payment at Counter")
        
        # UC10: View Pending Orders in Kitchen Queue
        test_endpoint('GET', f'{BASE_URL}/api/kitchen/order-queue', description="UC10: View Pending Orders in Kitchen Queue")
        
        # UC 11: Update Order Status to in preparation
        test_endpoint('PUT', f'{BASE_URL}/api/kitchen/update-order-status/{order_id1}',
                     data={'status': OrderStatus.PREPARING.value},
                     description="UC11: Update Order Status to in preparation")
        
        # UC 12: Update Order Status to ready for pickup
        test_endpoint('PUT', f'{BASE_URL}/api/kitchen/update-order-status/{order_id1}',
                     data={'status': OrderStatus.READY.value},
                     description="UC12: Update Order Status to ready for pickup")
        
        # UC 13: Add new Menu Item (Admin)
        test_endpoint('POST', f'{BASE_URL}/api/menu/items',
                     data={
                         'name': 'Veggie Burger',
                         'price': 5.99,
                         'category': 'Burgers',
                         'description': 'A delicious veggie burger with lettuce and tomato.'
                     },
                     description="UC13: Add New Menu Item (Admin)")
        
        # UC 14: Update Existing Menu Item (Admin)
        test_endpoint('PUT', f'{BASE_URL}/api/menu/items/1',
                     data={
                         'price': 6.49,
                         'description': 'Updated description for Classic Burger.'
                     },
                     description="UC14: Update Existing Menu Item (Admin)")
        
        # UC 15: View Daily Sales Report (Admin)
        today = datetime.now().strftime('%Y-%m-%d')
        test_endpoint('GET', f'{BASE_URL}/api/reports/sales-summary/{today}', description="UC15: View Daily Sales Report (Admin)")
        
    print("\n" + "="*60)
    print("API Testing Complete!")
    print("="*60)

if __name__ == '__main__':
    main()

