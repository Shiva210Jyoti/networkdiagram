from networkdiagram.networkdiagram import CriticalPathMethod

def test_validations():
    cpm = CriticalPathMethod()
    
    # Test 1: Empty name
    try:
        cpm.add_activity('', 5)
        print("❌ Test 1 failed")
    except ValueError as e:
        print(f"✅ Test 1 passed: {e}")
    
    # Test 2: Negative duration
    try:
        cpm.add_activity('A', -5)
        print("❌ Test 2 failed")
    except ValueError as e:
        print(f"✅ Test 2 passed: {e}")
    
    # Test 3: Duplicate name
    try:
        cpm.add_activity('A', 3)
        cpm.add_activity('A', 4)
        print("❌ Test 3 failed")
    except ValueError as e:
        print(f"✅ Test 3 passed: {e}")
    
    # Test 4: Empty activities list
    try:
        cpm.add_activities_relations([], [], [])
        print("❌ Test 4 failed")
    except ValueError as e:
        print(f"✅ Test 4 passed: {e}")
    
    # Test 5: Mismatched lengths
    try:
        cpm.add_activities_relations(['A', 'B'], [3], ['-', '-'])
        print("❌ Test 5 failed")
    except ValueError as e:
        print(f"✅ Test 5 passed: {e}")

if __name__ == "__main__":
    test_validations()