# Test Fixes Guide

## Common Test Issues and Solutions

### Issue 1: Import Errors
**Solution**: Make sure you're in the backend directory and have installed all dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Issue 2: Database Not Initialized
**Solution**: Tests use in-memory database, but make sure the test fixtures are working. The `conftest.py` should handle this automatically.

### Issue 3: Status Code Mismatches
**Solution**: Some endpoints return different status values. Fixed in test files:
- Welcome endpoint returns `'ready'` not `'success'`

### Issue 4: Missing Test Data
**Solution**: Tests use fixtures that create sample data automatically. If tests fail due to missing data, check that `sample_menu_items` fixture is working.

## Running Tests

### First Time Setup
```bash
cd backend
pip install -r requirements.txt
```

### Run Tests
```bash
# Activate virtual environment if using one
source venv/bin/activate  # or: . venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_uc1_start_system.py -v

# Run with more details
pytest tests/ -v -s

# Run and see coverage
pytest tests/ --cov=. --cov-report=term-missing
```

## If Tests Still Fail

1. **Check Python version**: Should be Python 3.8+
   ```bash
   python3 --version
   ```

2. **Reinstall dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check database**: Tests use in-memory DB, but verify imports work:
   ```bash
   python3 -c "from database import db; print('OK')"
   ```

4. **Run a single test** to isolate the issue:
   ```bash
   pytest tests/test_uc1_start_system.py::TestUC1StartSystem::test_welcome_endpoint -v
   ```

