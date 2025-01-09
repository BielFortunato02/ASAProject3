import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD


def solve_toy_distribution(input_data):
    # Parse Input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read Factory Data
    factories = []
    factory_dict = {}
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories.append((factory_id, country_id, stock))
        factory_dict[factory_id] = (country_id, stock)

    # Read Country Data
    countries = []
    country_limits = {}
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries.append((country_id, max_export, min_delivery))
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
            x[child_id, factory_id] = LpVariable(f"x_{child_id}_{factory_id}", cat='Binary')

    # Objective Function: Maximize satisfied children
    model += lpSum(x[child_id, factory_id] for child_id, factory_id in x)

    # Constraints

    # Each child gets at most one gift
    for child in children:
        child_id, _, factories_list = child
        model += lpSum(x[child_id, factory_id] for factory_id in factories_list) <= 1

    # Factory stock constraints
    for factory_id, (_, stock) in factory_dict.items():
        model += lpSum(x[child_id, factory_id] for child_id, _, factories_list in children if factory_id in factories_list) <= stock

    # Country constraints: Maximum exports and minimum deliveries
    for country_id, (max_export, min_delivery) in country_limits.items():
        country_factories = [factory_id for factory_id, (c_id, _) in factory_dict.items() if c_id == country_id]
        country_assignments = lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories)
        
        model += country_assignments <= max_export  # Maximum exports
        model += country_assignments >= min_delivery  # Minimum deliveries

    # Solve the Model
    model.solve(PULP_CBC_CMD(msg=False))

    # Output Result
    if LpStatus[model.status] == 'Optimal':
        print(sum(1 for child_id, factory_id in x if x[child_id, factory_id].varValue == 1))
    else:
        print(-1)


if __name__ == "__main__":
    # Read input from stdin
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)


'''
Hint:

T05

1 test with Time Limit Exceeded 16 tests with Accepted 17 tests with Wrong Answer1 test with Time Limit ExceededObservation of Time Limit Exceeded

(test T06): Time Limit Exceeded
'''