import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD

def solve_toy_distribution(input_data):
    # Parse Input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read Factory Data
    factories = {}
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories[factory_id] = (country_id, stock)

    # Read Country Data
    countries = {}
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries[country_id] = (max_export, min_delivery)

    # Read Children's Requests
    children = []
    for i in range(n + 1 + m, len(lines)):
        request = list(map(int, lines[i].split()))
        child_id, country_id, factories_list = request[0], request[1], request[2:]
        children.append((child_id, country_id, factories_list))

    # Linear Programming Model
    model = LpProblem(name="gift_distribution", sense=LpMaximize)

    # Decision Variables: Only create variables for valid combinations
    x = {}
    for child_id, _, factories_list in children:
        for factory_id in factories_list:
            if factory_id in factories:  # Ensure the factory exists
                x[child_id, factory_id] = LpVariable(f"x_{child_id}_{factory_id}", cat='Binary')

    # Objective Function: Maximize satisfied children
    model += lpSum(x[child_id, factory_id] for child_id, factory_id in x)

    # Constraints

    # Each child gets at most one gift
    for child_id, _, factories_list in children:
        model += lpSum(x[child_id, factory_id] for factory_id in factories_list if (child_id, factory_id) in x) <= 1

    # Factory stock constraints
    for factory_id, (_, stock) in factories.items():
        model += lpSum(x[child_id, factory_id] for child_id, _, factories_list in children if (child_id, factory_id) in x) <= stock

    # Country constraints: Maximum exports and minimum deliveries
    for country_id, (max_export, min_delivery) in countries.items():
        country_factories = [factory_id for factory_id, (c_id, _) in factories.items() if c_id == country_id]
        country_assignments = lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories)

        model += country_assignments <= max_export  # Maximum exports
        model += country_assignments >= min_delivery  # Minimum deliveries

    # Solve the Model with solver optimizations
    model.solve(PULP_CBC_CMD(msg=False, timeLimit=30))

    # Output Result
    if LpStatus[model.status] == 'Optimal':
        satisfied_children = sum(1 for child_id, factory_id in x if x[child_id, factory_id].varValue == 1)
        print(satisfied_children)
    else:
        print(-1)

if __name__ == "__main__":
    # Read input from stdin
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)
