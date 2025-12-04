# Fast Food Ordering System - Backend

## Overview
Flask-based REST API backend implementing UC1-UC7 use cases for the Fast Food Ordering System.

## Project Structure

```
backend/
├── app.py                 # Main Flask application entry point
├── config.py              # Configuration settings
├── database.py            # Database initialization
├── requirements.txt       # Python dependencies
├── seed_data.py           # Script to populate sample menu data
├── models/                # Data models (SQLAlchemy)
│   ├── __init__.py
│   ├── menu_item.py       # MenuItem model
│   ├── order.py           # Order model
│   ├── order_item.py      # OrderItem model
│   └── payment.py         # Payment model
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── menu_service.py    # Menu operations
│   ├── order_service.py   # Order operations
│   └── payment_service.py # Payment operations
└── routes/                # API routes (controllers)
    ├── __init__.py
    ├── main.py            # Main/test routes
    ├── menu_routes.py      # Menu API endpoints (UC1, UC2, UC3)
    ├── order_routes.py    # Order API endpoints (UC4, UC5, UC6)
    └── payment_routes.py  # Payment API endpoints (UC7)
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database and seed sample data:
```bash
python seed_data.py
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5001` (default)
Note: Port can be changed via `PORT` environment variable. Port 5000 is often used by AirPlay on macOS.

## API Endpoints

### UC1: Start the System
- `GET /api/menu/welcome` - Get welcome message

### UC2: Browse Menu
- `GET /api/menu/categories` - Get all menu categories
- `GET /api/menu/items` - Get all menu items (optional: `?category=Burgers`)

### UC3: View Item Details and Customize
- `GET /api/menu/items/<item_id>` - Get menu item details
- `POST /api/menu/items/<item_id>/calculate-price` - Calculate price with customizations

### UC4: Add Item to Order
- `POST /api/orders` - Create new order
- `POST /api/orders/<order_id>/items` - Add item to order

### UC5: Review and Edit Order
- `GET /api/orders/<order_id>` - Get order details
- `PUT /api/orders/<order_id>/items/<item_id>` - Update item quantity
- `DELETE /api/orders/<order_id>/items/<item_id>` - Remove item from order

### UC6: Confirm Order and Proceed to Payment
- `POST /api/orders/<order_id>/finalize` - Finalize order with payment method

### UC7: Complete Payment at System
- `POST /api/payments/process-system` - Process card payment at kiosk

## Data Models

### MenuItem
- Represents menu items with categories, prices, and customization options

### Order
- Represents customer orders with status tracking
- Statuses: Pending, In Preparation, Ready, Completed, Cancelled
- Payment Statuses: Pending, Pending Payment at Counter, Paid, Failed, Refunded

### OrderItem
- Represents items within an order with quantities and customizations

### Payment
- Represents payment transactions
- Methods: Card at System, Cash at Counter, Card at Counter
- Statuses: Pending, Processing, Approved, Failed, Refunded

## Architecture

The backend follows a three-layer architecture:
- **Presentation Layer**: Routes (Flask blueprints)
- **Application Layer**: Services (business logic)
- **Domain Layer**: Models (data persistence)

## Database

Uses SQLite by default (configurable via `DATABASE_URL` environment variable).
Database file: `fastfood.db` (created automatically on first run)

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_uc1_start_system.py -v
```

### Test Structure

- **Unit Tests**: Individual use case tests (UC1-UC7)
- **Integration Tests**: Complete order flow tests
- **Test Database**: In-memory SQLite (fresh for each test)

See `TESTING.md` for detailed testing documentation.

## Quick Start

See `QUICKSTART.md` for step-by-step setup and example API calls.
