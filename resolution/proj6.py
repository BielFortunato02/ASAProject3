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
        child_id = request[0]
        factories_list = request[2:]
        children.append((child_id, request[1], factories_list))

    # Linear Programming Model
    model = LpProblem(name="gift_distribution", sense=LpMaximize)

    # Decision Variables: Only create variables for valid combinations
    x = {
        (child_id, factory_id): LpVariable(f"x_{child_id}_{factory_id}", cat='Binary')
        for child_id, _, factories_list in children
        for factory_id in factories_list
    }

    # Objective Function: Maximize satisfied children
    model += lpSum(x[child_id, factory_id] for child_id, factory_id in x)

    # Constraints

    # Each child gets at most one gift
    for child_id, _, factories_list in children:
        model += lpSum(x[child_id, factory_id] for factory_id in factories_list) <= 1

    # Factory stock constraints
    for factory_id, (_, stock) in factories.items():
        model += lpSum(x[child_id, factory_id] for child_id, _, factories_list in children if factory_id in factories_list) <= stock

    # Country constraints: Maximum exports and minimum deliveries
    for country_id, (max_export, min_delivery) in countries.items():
        # Gather all factories in this country
        country_factories = [fid for fid, (cid, _) in factories.items() if cid == country_id]

        # Maximum exports
        model += lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories) <= max_export

        # Minimum deliveries
        model += lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories) >= min_delivery

    # Solve the Model
    solver = PULP_CBC_CMD(msg=False, timeLimit=60)
    model.solve(solver)

    # Output Result
    if LpStatus[model.status] == 'Optimal':
        print(sum(1 for child_id, factory_id in x if x[child_id, factory_id].varValue == 1))
    else:
        print(-1)

if __name__ == "__main__":
    # Read input from stdin
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)
