import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD

def solve_toy_distribution(input_data):
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    factory_dict = {}
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factory_dict[factory_id] = (country_id, stock)

    country_limits = {}
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        country_limits[country_id] = (max_export, min_delivery)

    children = []
    for i in range(n + 1 + m, len(lines)):
        request = list(map(int, lines[i].split()))
        children.append((request[0], request[1], request[2:]))

    model = LpProblem(name="gift_distribution", sense=LpMaximize)
    x = {}
    for child in children:
        child_id, _, factories_list = child
        for factory_id in factories_list:
            if factory_id in factory_dict:
                x[child_id, factory_id] = LpVariable(f"x_{child_id}_{factory_id}", cat='Binary')

    model += lpSum(x[child_id, factory_id] for child_id, factory_id in x)

    for child in children:
        child_id, _, factories_list = child
        model += lpSum(x[child_id, factory_id] for factory_id in factories_list if (child_id, factory_id) in x) <= 1

    for factory_id, (_, stock) in factory_dict.items():
        model += lpSum(x[child_id, factory_id] for child_id, _, factories_list in children if (child_id, factory_id) in x) <= stock

    for country_id, (max_export, min_delivery) in country_limits.items():
        country_factories = [factory_id for factory_id, (c_id, _) in factory_dict.items() if c_id == country_id]
        country_assignments = lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories)

        # Adjusted to prevent conflicting constraints
        total_factory_stock = sum(factory_dict[f][1] for f in country_factories)
        feasible_min_delivery = min(min_delivery, total_factory_stock)
        model += country_assignments <= max_export
        model += country_assignments >= feasible_min_delivery

    model.solve(PULP_CBC_CMD(msg=True))
    
    # Debugging: Print all variables and constraints
    print("Variables:")
    for var in model.variables():
        print(f"{var.name}: {var.varValue}")

    print("\nConstraints:")
    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint}")

    return sum(1 for child_id, factory_id in x if x[child_id, factory_id].varValue == 1) if LpStatus[model.status] == 'Optimal' else -1

# Define the test cases for simulation
def test_code():
    test_cases = [
        {
            "input": """3 2 5\n1 1 2\n2 1 2\n3 2 2\n1 2 2\n2 2 1\n1 1 1 2\n2 1 2 3\n3 2 3 1\n4 2 2 3\n5 1 1""",
            "expected": 5
        },
        {
            "input": """10 5 20\n1 1 5\n2 1 5\n3 2 5\n4 2 5\n5 3 5\n6 3 5\n7 4 5\n8 4 5\n9 5 5\n10 5 5\n1 10 2\n2 10 2\n3 10 2\n4 10 2\n5 10 2\n1 1 1 2 3\n2 1 2 3 4\n3 2 3 4 5\n4 2 4 5 6\n5 3 5 6 7""",
            "expected": 20
        }
    ]

    results = []
    for idx, test in enumerate(test_cases, 1):
        print(f"Running Test Case {idx}...")
        output = solve_toy_distribution(test['input'])
        results.append({
            "expected": test['expected'],
            "output": output,
            "pass": output == test['expected']
        })
    
    print("\nTest Results:")
    for result in results:
        print(result)

# Run Tests
if __name__ == "__main__":
    test_code()
