"""
Integration tests for complete order flow (UC1-UC7)
"""
import pytest
from tests.conftest import app, client, sample_menu_items

class TestFullOrderFlow:
    """Integration tests for complete order flow"""
    
    def test_complete_order_flow_card_payment(self, client, sample_menu_items):
        """
        Test complete flow from welcome to payment completion
        UC1 -> UC2 -> UC3 -> UC4 -> UC5 -> UC6 -> UC7
        """
        # UC1: Start the System
        welcome_response = client.get('/api/menu/welcome')
        assert welcome_response.status_code == 200
        
        # UC2: Browse Menu
        categories_response = client.get('/api/menu/categories')
        assert categories_response.status_code == 200
        categories = categories_response.get_json()['categories']
        assert 'Burgers' in categories
        
        items_response = client.get('/api/menu/items?category=Burgers')
        assert items_response.status_code == 200
        items = items_response.get_json()['items']
        assert len(items) > 0
        burger_id = items[0]['id']
        
        # UC3: View Item Details and Customize
        item_details = client.get(f'/api/menu/items/{burger_id}')
        assert item_details.status_code == 200
        item = item_details.get_json()['item']
        
        price_calc = client.post(
            f'/api/menu/items/{burger_id}/calculate-price',
            json={'customizations': {'size': 'large'}}
        )
        assert price_calc.status_code == 200
        customized_price = price_calc.get_json()['customized_price']
        
        # UC4: Add Item to Order
        order_response = client.post('/api/orders')
        assert order_response.status_code == 201
        order_id = order_response.get_json()['order']['id']
        
        add_item = client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': burger_id,
                'quantity': 2,
                'customizations': {'size': 'large'}
            }
        )
        assert add_item.status_code == 201
        
        # UC5: Review and Edit Order
        review_order = client.get(f'/api/orders/{order_id}')
        assert review_order.status_code == 200
        order = review_order.get_json()['order']
        assert len(order['order_items']) == 1
        assert order['subtotal'] > 0
        
        # UC6: Confirm Order and Proceed to Payment
        finalize = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'card_at_system'}
        )
        assert finalize.status_code == 200
        finalized_order = finalize.get_json()['order']
        assert finalized_order['payment_method'] == 'card_at_system'
        assert finalized_order['total'] > 0
        
        # UC7: Complete Payment at System
        payment = client.post(
            '/api/payments/process-system',
            json={'order_id': order_id}
        )
        assert payment.status_code == 200
        payment_data = payment.get_json()
        assert payment_data['payment']['status'] == 'Approved'
        assert payment_data['order']['payment_status'] == 'Paid'
        assert payment_data['order']['status'] == 'Pending'  # Ready for kitchen
        assert 'order_number' in payment_data
    
    def test_complete_order_flow_counter_payment(self, client, sample_menu_items):
        """
        Test complete flow with counter payment option
        """
        # Create order and add items
        order_response = client.post('/api/orders')
        order_id = order_response.get_json()['order']['id']
        
        # Add multiple items
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[0].id,
                'quantity': 1
            }
        )
        client.post(
            f'/api/orders/{order_id}/items',
            json={
                'menu_item_id': sample_menu_items[1].id,
                'quantity': 2
            }
        )
        
        # Finalize with counter payment
        finalize = client.post(
            f'/api/orders/{order_id}/finalize',
            json={'payment_method': 'cash_at_counter'}
        )
        assert finalize.status_code == 200
        
        order = finalize.get_json()['order']
        assert order['payment_status'] == 'Pending Payment at Counter'
        
        # Get order by number
        order_number = order['order_number']
        get_by_number = client.get(f'/api/orders/number/{order_number}')
        assert get_by_number.status_code == 200
        assert get_by_number.get_json()['order']['order_number'] == order_number

