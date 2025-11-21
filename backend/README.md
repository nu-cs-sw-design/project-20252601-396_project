# Fast Food Ordering System - Backend

Flask backend API for the Fast Food Ordering System.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Project Structure

- `app.py` - Main Flask application entry point
- `routes/` - API route handlers
  - `main.py` - Main API routes
- `models/` - Data models and database schemas
- `services/` - Business logic layer
- `utils/` - Utility functions and helpers

## API Endpoints

- `GET /` - Health check endpoint
- `GET /api/test` - Test API endpoint

## Development

The Flask app runs in debug mode by default. To change this, modify the `app.py` file or use environment variables.

