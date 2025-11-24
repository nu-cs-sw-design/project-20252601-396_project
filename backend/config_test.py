"""
Test configuration settings
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

class TestConfig:
    """Test configuration - uses in-memory SQLite database"""
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    JSONIFY_PRETTYPRINT_REGULAR = True

