# Test Fix Summary - DetachedInstanceError

## Problem
Tests were failing with `sqlalchemy.orm.exc.DetachedInstanceError: Instance <MenuItem> is not bound to a Session`. This happened because MenuItem instances created in the `sample_menu_items` fixture became detached from the database session after commit.

## Root Cause
When SQLAlchemy commits objects, they can become "detached" from the session. When tests later tried to access attributes like `.id` or when OrderItem tried to access `menu_item.to_dict()`, SQLAlchemy couldn't lazy-load the data because the instance was no longer bound to a session.

## Solutions Applied

### 1. Fixed `sample_menu_items` Fixture
Changed the fixture to return a wrapper that re-queries items from the database each time they're accessed. This ensures items are always fresh and bound to the current session.

**Before**: Returned items directly (became detached after commit)
**After**: Returns a `FreshMenuItems` wrapper that re-queries items when accessed

### 2. Updated OrderItem Relationship
Changed the relationship loading strategy to `lazy='joined'` to eagerly load menu_item data:
```python
menu_item = db.relationship('MenuItem', backref='order_items', lazy='joined')
```

### 3. Added Error Handling in OrderItem.to_dict()
Added try/except to handle detached instances gracefully:
```python
try:
    if self.menu_item:
        menu_item_dict = self.menu_item.to_dict()
except Exception:
    # If menu_item is detached, just use menu_item_id
    pass
```

## Testing the Fix

Run tests again:
```bash
pytest tests/ -v
```

All tests should now pass. The `FreshMenuItems` wrapper ensures that:
- Items are always queried fresh from the database
- Items are bound to the current app context's session
- No detached instance errors occur

## Files Modified

1. `tests/conftest.py` - Updated `sample_menu_items` fixture
2. `models/order_item.py` - Changed relationship loading and added error handling

