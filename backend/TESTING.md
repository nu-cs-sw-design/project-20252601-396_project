# Backend Testing Guide

## Overview
This document describes the testing methodology and test suite for the Fast Food Ordering System backend (UC1-UC7).

## Test Structure

The test suite is organized by use case:
- `test_uc1_start_system.py` - Tests for UC1: Start the System
- `test_uc2_browse_menu.py` - Tests for UC2: Browse Menu
- `test_uc3_item_details.py` - Tests for UC3: View Item Details and Customize
- `test_uc4_add_item_to_order.py` - Tests for UC4: Add Item to Order
- `test_uc5_review_edit_order.py` - Tests for UC5: Review and Edit Order
- `test_uc6_confirm_order.py` - Tests for UC6: Confirm Order and Proceed to Payment
- `test_uc7_payment.py` - Tests for UC7: Complete Payment at System
- `test_integration_full_flow.py` - Integration tests for complete order flow

## Test Configuration

- **Test Database**: In-memory SQLite database (created fresh for each test)
- **Test Framework**: pytest
- **Coverage**: pytest-cov for code coverage reporting

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
# Using pytest directly
pytest tests/ -v

# Using the test runner script
python run_tests.py
```

### Run Specific Test File
```bash
pytest tests/test_uc1_start_system.py -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test Class
```bash
pytest tests/test_uc1_start_system.py::TestUC1StartSystem -v
```

### Run Specific Test Method
```bash
pytest tests/test_uc1_start_system.py::TestUC1StartSystem::test_welcome_endpoint -v
```

## Test Coverage

Each use case is tested with:
1. **Happy Path Tests**: Normal flow with valid inputs
2. **Error Handling Tests**: Invalid inputs, missing data, edge cases
3. **Boundary Tests**: Edge cases and boundary conditions
4. **Integration Tests**: Complete flows across multiple use cases

## Test Data

Test fixtures provide:
- Sample menu items (Burgers, Sides, Drinks)
- Fresh database for each test (no test pollution)
- Isolated test environment

## Test Execution Flow

1. **Setup**: Create test app with in-memory database
2. **Execute**: Run test against API endpoints
3. **Assert**: Verify response status, data structure, and business logic
4. **Teardown**: Clean up database (automatic with fixtures)

## Example Test Execution

```bash
$ pytest tests/ -v

tests/test_uc1_start_system.py::TestUC1StartSystem::test_welcome_endpoint PASSED
tests/test_uc1_start_system.py::TestUC1StartSystem::test_health_check PASSED
tests/test_uc2_browse_menu.py::TestUC2BrowseMenu::test_get_categories PASSED
...
```

## Continuous Integration

Tests can be integrated into CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=. --cov-report=xml
```

## Test Maintenance

- Add new tests when adding features
- Update tests when requirements change
- Keep test data realistic and representative
- Ensure tests are independent and can run in any order

## Troubleshooting

### Import Errors
- Ensure you're running from the backend directory
- Check that all dependencies are installed

### Database Errors
- Tests use in-memory database, no file cleanup needed
- Each test gets a fresh database

### Test Failures
- Check test output for specific assertion failures
- Verify API endpoints are correctly implemented
- Ensure test data matches expected structure

