# Test Case Generator for Toy Distribution Problem

def generate_test_cases():
    test_cases = []

    # Basic Feasibility Test
    test_cases.append(("Basic Feasibility",
        "1 1 1\n"  # 1 factory, 1 country, 1 child
        "1 1 1\n"  # Factory ID 1, Country ID 1, Stock 1
        "1 1 1\n"  # Country ID 1, Max Export 1, Min Delivery 1
        "1 1 1\n"  # Child ID 1, Country ID 1, Factory List [1]
    ))

    # Edge Case: No valid factories
    test_cases.append(("No Valid Factories",
        "2 1 2\n"  # 2 factories, 1 country, 2 children
        "1 1 1\n"  # Factory ID 1, Country ID 1, Stock 1
        "2 1 1\n"  # Factory ID 2, Country ID 1, Stock 1
        "1 2 1\n"  # Country ID 1, Max Export 2, Min Delivery 1
        "1 1 3\n"  # Child ID 1, Country ID 1, Factory List [3] (invalid)
        "2 1 3\n"  # Child ID 2, Country ID 1, Factory List [3] (invalid)
    ))

    # Complex Scenario
    test_cases.append(("Complex Scenario",
        "3 2 5\n"  # 3 factories, 2 countries, 5 children
        "1 1 2\n"  # Factory ID 1, Country ID 1, Stock 2
        "2 1 2\n"  # Factory ID 2, Country ID 1, Stock 2
        "3 2 2\n"  # Factory ID 3, Country ID 2, Stock 2
        "1 2 2\n"  # Country ID 1, Max Export 2, Min Delivery 2
        "2 2 1\n"  # Country ID 2, Max Export 2, Min Delivery 1
        "1 1 1 2\n"  # Child ID 1, Country ID 1, Factories [1, 2]
        "2 1 2 3\n"  # Child ID 2, Country ID 1, Factories [2, 3]
        "3 2 3 1\n"  # Child ID 3, Country ID 2, Factories [3, 1]
        "4 2 2 3\n"  # Child ID 4, Country ID 2, Factories [2, 3]
        "5 1 1\n"  # Child ID 5, Country ID 1, Factory [1]
    ))

    # Stress Test
    test_cases.append(("Stress Test",
        "10 5 20\n"  # 10 factories, 5 countries, 20 children
        "1 1 5\n"  # Factory ID 1, Country ID 1, Stock 5
        "2 1 5\n"  # Factory ID 2, Country ID 1, Stock 5
        "3 2 5\n"  # Factory ID 3, Country ID 2, Stock 5
        "4 2 5\n"  # Factory ID 4, Country ID 2, Stock 5
        "5 3 5\n"  # Factory ID 5, Country ID 3, Stock 5
        "6 3 5\n"  # Factory ID 6, Country ID 3, Stock 5
        "7 4 5\n"  # Factory ID 7, Country ID 4, Stock 5
        "8 4 5\n"  # Factory ID 8, Country ID 4, Stock 5
        "9 5 5\n"  # Factory ID 9, Country ID 5, Stock 5
        "10 5 5\n"  # Factory ID 10, Country ID 5, Stock 5
        "1 10 2\n"  # Country ID 1, Max Export 10, Min Delivery 2
        "2 10 2\n"  # Country ID 2, Max Export 10, Min Delivery 2
        "3 10 2\n"  # Country ID 3, Max Export 10, Min Delivery 2
        "4 10 2\n"  # Country ID 4, Max Export 10, Min Delivery 2
        "5 10 2\n"  # Country ID 5, Max Export 10, Min Delivery 2
        "1 1 1 2 3\n"  # Child ID 1, Country ID 1, Factories [1, 2, 3]
        "2 1 2 3 4\n"  # Child ID 2, Country ID 1, Factories [2, 3, 4]
        "...\n"  # Similar lines for all children, omitted for brevity
    ))

    return test_cases

# Function to print test cases in the correct format
def print_test_cases():
    test_cases = generate_test_cases()
    for name, case in test_cases:
        print(f"Test: {name}\n")
        print(case)
        print("\n" + "="*20 + "\n")

if __name__ == "__main__":
    print_test_cases()
