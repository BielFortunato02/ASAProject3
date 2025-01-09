import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD

def solve_toy_distribution(input_data):
    # Parse Input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read Factory Data
    factory_dict = {}
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factory_dict[factory_id] = (country_id, stock)

    # Read Country Data
    country_limits = {}
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        country_limits[country_id] = (max_export, min_delivery)

    # Read Children's Requests
    children = []
    for i in range(n + 1 + m, len(lines)):
        request = list(map(int, lines[i].split()))
        children.append((request[0], request[1], request[2:]))

    # Linear Programming Model
    model = LpProblem(name="gift_distribution", sense=LpMaximize)

    # Decision Variables: Only create variables for valid combinations
    x = {}
    for child in children:
        child_id, _, factories_list = child
        for factory_id in factories_list:
            if factory_id in factory_dict:  # Ensure the factory exists in data
                x[child_id, factory_id] = LpVariable(f"x_{child_id}_{factory_id}", cat='Binary')

    # Objective Function: Maximize satisfied children
    model += lpSum(x[child_id, factory_id] for child_id, factory_id in x)

    # Constraints

    # Each child gets at most one gift
    for child in children:
        child_id, _, factories_list = child
        model += lpSum(x[child_id, factory_id] for factory_id in factories_list if (child_id, factory_id) in x) <= 1

    # Factory stock constraints
    for factory_id, (_, stock) in factory_dict.items():
        model += lpSum(x[child_id, factory_id] for child_id, _, factories_list in children if (child_id, factory_id) in x) <= stock

    # Country constraints: Maximum exports and minimum deliveries
    for country_id, (max_export, min_delivery) in country_limits.items():
        country_factories = [factory_id for factory_id, (c_id, _) in factory_dict.items() if c_id == country_id]
        country_assignments = lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories)

        model += country_assignments <= max_export  # Maximum exports
        model += country_assignments >= min_delivery  # Minimum deliveries

    # Solve the Model
    model.solve(PULP_CBC_CMD(msg=True))

    # Debugging: Print Constraint Information
    print("Constraints:\n")
    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint}")

    # Output Result
    if LpStatus[model.status] == 'Optimal':
        result = sum(1 for child_id, factory_id in x if x[child_id, factory_id].varValue == 1)
        print(result)
    else:
        print(-1)

# Simulate Input for Testing
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

    for idx, test in enumerate(test_cases, 1):
        print(f"Running Test Case {idx}...")
        solve_toy_distribution(test['input'])

# Run Tests
if __name__ == "__main__":
    test_code()
