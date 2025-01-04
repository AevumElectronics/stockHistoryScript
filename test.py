# test_script.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def main():
    # Test cases
    print("Running tests...")
    
    assert add(2, 3) == 5, "Test failed: 2 + 3 should equal 5"
    assert subtract(5, 2) == 3, "Test failed: 5 - 2 should equal 3"

    print("All tests passed!")

if __name__ == "__main__":
    main()
