# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Setup Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database and Seed Data
```bash
python seed_data.py
```

This will:
- Create the database file (`fastfood.db`)
- Populate it with sample menu items (Burgers, Sides, Drinks)

### 3. Run the Backend Server
```bash
python app.py
```

The API will be available at `http://localhost:5001` (default)
Note: Port can be changed via `PORT` environment variable. Port 5000 is often used by AirPlay on macOS.

### 4. Test the API

#### Health Check
```bash
curl http://localhost:5001/
```

#### UC1: Welcome Message
```bash
curl http://localhost:5001/api/menu/welcome
```

#### UC2: Get Categories
```bash
curl http://localhost:5001/api/menu/categories
```

#### UC2: Get Menu Items
```bash
curl http://localhost:5001/api/menu/items
curl http://localhost:5001/api/menu/items?category=Burgers
```

#### UC3: Get Item Details
```bash
curl http://localhost:5001/api/menu/items/1
```

#### UC4: Create Order and Add Item
```bash
# Create order
curl -X POST http://localhost:5001/api/orders

# Add item (replace ORDER_ID and ITEM_ID)
curl -X POST http://localhost:5001/api/orders/1/items \
  -H "Content-Type: application/json" \
  -d '{"menu_item_id": 1, "quantity": 2, "customizations": {"size": "large"}}'
```

#### UC5: Review Order
```bash
curl http://localhost:5001/api/orders/1
```

#### UC6: Finalize Order
```bash
curl -X POST http://localhost:5001/api/orders/1/finalize \
  -H "Content-Type: application/json" \
  -d '{"payment_method": "card_at_system"}'
```

#### UC7: Process Payment
```bash
curl -X POST http://localhost:5001/api/payments/process-system \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_uc1_start_system.py -v
```

## Troubleshooting

### Port Already in Use
The default port is 5001 to avoid conflicts with AirPlay on macOS. To use a different port:
```bash
PORT=8000 python3 app.py
```

Or modify `app.py` to change the default port.

### Database Issues
Delete `fastfood.db` and run `python seed_data.py` again to reset.

### Import Errors
Make sure you're running commands from the `backend` directory.

## API Documentation

See `README.md` for complete API documentation.

## Testing Documentation

See `TESTING.md` for detailed testing information.

