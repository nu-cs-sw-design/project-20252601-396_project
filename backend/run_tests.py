#!/usr/bin/env python3
"""
Test runner script for backend tests
"""
import sys
import subprocess
import os

def run_tests():
    """Run all tests using pytest"""
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Run pytest
    result = subprocess.run(
        ['pytest', 'tests/', '-v', '--tb=short'],
        cwd=backend_dir
    )
    
    return result.returncode

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)

