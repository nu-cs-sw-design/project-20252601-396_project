# Solutions for Common Issues

## Issue 1: How to See API Results

### Quick Test (Easiest Method)

1. **Make sure your server is running** (you should see it in terminal)

2. **Open a browser** and go to:
   ```
   http://localhost:5001/
   ```
   You should see: `{"status": "ok", "message": "Fast Food Ordering System API"}`

3. **Test the welcome endpoint**:
   ```
   http://localhost:5001/api/menu/welcome
   ```

4. **Or use the test script** (recommended):
   ```bash
   # In a new terminal (while app.py is running)
   cd backend
   python3 test_api.py
   ```

### Using curl (Terminal)
```bash
# Health check
curl http://localhost:5001/

# Welcome
curl http://localhost:5001/api/menu/welcome

# Categories
curl http://localhost:5001/api/menu/categories

# Items
curl http://localhost:5001/api/menu/items
```

## Issue 2: Fixing pytest Test Failures

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run Tests with Details
```bash
# See what's failing
pytest tests/ -v --tb=short

# Or run one test file at a time
pytest tests/test_uc1_start_system.py -v
```

### Step 3: Common Fixes

#### Fix 1: Missing pytest
```bash
pip install pytest pytest-cov
```

#### Fix 2: Import Errors
If you see import errors, make sure you're in the backend directory:
```bash
cd backend
pytest tests/ -v
```

#### Fix 3: Database Issues
Tests use in-memory database automatically. If you see database errors, check that `conftest.py` is correct.

#### Fix 4: Status Code Mismatches
I've already fixed the welcome endpoint test - it now expects `'ready'` instead of `'success'`.

### Step 4: Run Tests in Virtual Environment
If you're using a virtual environment:
```bash
# Activate venv
source venv/bin/activate  # or: . venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Quick Verification

### Verify Server is Running
```bash
curl http://localhost:5001/
```
Should return: `{"status": "ok", "message": "Fast Food Ordering System API"}`

### Verify Database is Seeded
```bash
curl http://localhost:5001/api/menu/items
```
Should return a list of menu items (if you ran `python3 seed_data.py`)

### Verify Tests Can Run
```bash
pytest tests/test_uc1_start_system.py::TestUC1StartSystem::test_health_check -v
```
Should pass if everything is set up correctly.

## Still Having Issues?

1. **Check Python version**: `python3 --version` (should be 3.8+)
2. **Check if server is running**: Look for "Running on http://..." in terminal
3. **Check port**: Default is 5001, verify in `app.py`
4. **Check database**: Run `python3 seed_data.py` if you haven't
5. **Check imports**: Try `python3 -c "from app import create_app; print('OK')"`

## Need More Help?

See these files:
- `HOW_TO_TEST.md` - Detailed testing guide
- `TEST_FIXES.md` - Test troubleshooting
- `QUICKSTART.md` - Quick setup guide

