# How to Test the API

## Method 1: Using the Test Script (Easiest)

1. **Start the server** (in one terminal):
   ```bash
   cd backend
   python3 app.py
   ```

2. **Run the test script** (in another terminal):
   ```bash
   cd backend
   python3 test_api.py
   ```

This will test all endpoints automatically!

## Method 2: Using curl (Command Line)

### UC1: Start the System
```bash
# Health check
curl http://localhost:5001/

# Welcome message
curl http://localhost:5001/api/menu/welcome
```

### UC2: Browse Menu
```bash
# Get categories
curl http://localhost:5001/api/menu/categories

# Get all items
curl http://localhost:5001/api/menu/items

# Get items by category
curl http://localhost:5001/api/menu/items?category=Burgers
```

### UC3: View Item Details
```bash
# Get item details (replace 1 with actual item ID)
curl http://localhost:5001/api/menu/items/1

# Calculate price with customizations
curl -X POST http://localhost:5001/api/menu/items/1/calculate-price \
  -H "Content-Type: application/json" \
  -d '{"customizations": {"size": "large"}}'
```

### UC4: Add Item to Order
```bash
# Create order
curl -X POST http://localhost:5001/api/orders

# Add item (replace ORDER_ID with actual order ID from above)
curl -X POST http://localhost:5001/api/orders/1/items \
  -H "Content-Type: application/json" \
  -d '{"menu_item_id": 1, "quantity": 2, "customizations": {"size": "large"}}'
```

### UC5: Review Order
```bash
curl http://localhost:5001/api/orders/1
```

### UC6: Finalize Order
```bash
curl -X POST http://localhost:5001/api/orders/1/finalize \
  -H "Content-Type: application/json" \
  -d '{"payment_method": "card_at_system"}'
```

### UC7: Process Payment
```bash
curl -X POST http://localhost:5001/api/payments/process-system \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

## Method 3: Using Browser

Simply open these URLs in your browser:
- http://localhost:5001/
- http://localhost:5001/api/menu/welcome
- http://localhost:5001/api/menu/categories
- http://localhost:5001/api/menu/items

## Method 4: Using Postman or Insomnia

1. Import the endpoints
2. Set base URL: `http://localhost:5001`
3. Test each endpoint

## Method 5: Using Python requests

```python
import requests

BASE_URL = "http://localhost:5001"

# Test welcome
response = requests.get(f"{BASE_URL}/api/menu/welcome")
print(response.json())

# Test categories
response = requests.get(f"{BASE_URL}/api/menu/categories")
print(response.json())
```

## Expected Responses

### Welcome Endpoint
```json
{
  "message": "Welcome to Fast Food Ordering System",
  "status": "ready",
  "main_menu_available": true
}
```

### Categories Endpoint
```json
{
  "categories": ["Burgers", "Sides", "Drinks"],
  "status": "success"
}
```

### Items Endpoint
```json
{
  "items": [
    {
      "id": 1,
      "name": "Classic Burger",
      "price": 8.99,
      "category": "Burgers",
      ...
    }
  ],
  "status": "success"
}
```

## Troubleshooting

### "Connection refused" or "Could not connect"
- Make sure `app.py` is running
- Check the port (should be 5001 by default)
- Verify the URL is correct

### "404 Not Found"
- Make sure you seeded the database: `python3 seed_data.py`
- Check that menu items exist

### "500 Internal Server Error"
- Check the terminal running `app.py` for error messages
- Verify database is initialized

