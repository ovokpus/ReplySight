#!/usr/bin/env python3
"""
Test runner for ReplySight - runs all test scripts
"""

import sys
import os
import subprocess
from pathlib import Path

def run_test_script(script_path: Path) -> bool:
    """Run a single test script and return success status."""
    
    print(f"\n{'='*60}")
    print(f"Running: {script_path.name}")
    print(f"{'='*60}")
    
    try:
        # Run the test script using uv
        result = subprocess.run(
            ["uv", "run", "python", str(script_path)],
            cwd=script_path.parent.parent,  # Run from project root
            capture_output=False,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            print(f"✅ {script_path.name} PASSED")
        else:
            print(f"❌ {script_path.name} FAILED (exit code: {result.returncode})")
            
        return success
        
    except Exception as e:
        print(f"❌ Error running {script_path.name}: {e}")
        return False

def main():
    """Run all test scripts in the tests directory."""
    
    print("🚀 ReplySight Test Suite Runner")
    print("Running comprehensive backend tests...")
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    
    # Find all test scripts (excluding this runner and __init__.py)
    test_scripts = [
        f for f in tests_dir.glob("test_*.py") 
        if f.name != "run_all_tests.py"
    ]
    
    if not test_scripts:
        print("❌ No test scripts found!")
        return False
    
    print(f"Found {len(test_scripts)} test script(s)")
    
    # Run each test script
    results = []
    for script in sorted(test_scripts):
        success = run_test_script(script)
        results.append((script.name, success))
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for script_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{script_name:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("💥 Some tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 