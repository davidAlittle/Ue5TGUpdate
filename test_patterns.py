#!/usr/bin/env python3
"""
Test script for UE5 Update Monitor pattern matching
"""

import sys
import os

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ue5_monitor import UE5UpdateMonitor


def test_pattern_matching():
    """Test the pattern matching functionality"""
    
    # Create a monitor instance with dummy credentials for testing
    monitor = UE5UpdateMonitor(
        api_id=12345,
        api_hash="dummy",
        phone="+1234567890",
        channel="test"
    )
    
    # Test cases: (text, should_match)
    test_cases = [
        ("New UE 5.4 plugin update available!", True),
        ("Updated to Unreal Engine 5.3", True),
        ("Plugin released for UE5.2", True),
        ("Version 5.1 now available for download", False),  # No UE mention
        ("UE 5.0 marketplace update", True),
        ("New features in v5.4", False),  # No UE mention
        ("Just random text", False),
        ("Version 1.0 for Unity", False),  # No UE mention
        ("UE without version number", False),
        ("5.4 alone without context", False),
        ("Download UE5.4 now!", True),
        ("Unreal Engine 5.3 plugin released", True),
        ("UE5.1 available", True),  # Has UE and version
        ("Unreal Engine 4.27 update", True),  # Also matches UE4
    ]
    
    print("Testing UE5 Update Monitor Pattern Matching\n")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for text, expected in test_cases:
        result = monitor.is_update_message(text)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status}")
        print(f"Text: {text}")
        print(f"Expected: {expected}, Got: {result}")
    
    print("\n" + "=" * 60)
    print(f"\nResults: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = test_pattern_matching()
    sys.exit(0 if success else 1)
