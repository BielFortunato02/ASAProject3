import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

def solve_toy_distribution():
    # Read input
    input_data = sys.stdin.read().strip().splitlines()
    n, m, t = map(int, input_data[0].split())

    # Read Factory Data
    factories = []
    factory_dict = {}
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, input_data[i].split())
        factories.append((factory_id, country_id, stock))
        factory_dict[factory_id] = (country_id, stock)

    # Read Country Data
    countries = []
    country_limits = {}
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, input_data[i].split())
        countries.append((country_id, max_export, min_delivery))
        country_limits[country_id] = (max_export, min_delivery)

    # Read Children's Requests
    children = []
    for i in range(n + 1 + m, len(input_data)):
        request = list(map(int, input_data[i].split()))
        children.append((request[0], request[1], request[2:]))

    # Define the LP problem
    problem = LpProblem("Maximize_Satisfied_Children", LpMaximize)

    # Decision variables
    x = {}
    for child_id, _, factory_ids in children:
        for factory_id in factory_ids:
            x[child_id, factory_id] = LpVariable(f"x_{child_id}_{factory_id}", 0, 1, cat='Binary')

    # Objective function
    problem += lpSum(x[child_id, factory_id] for child_id, factory_id in x), "Total_Satisfied_Children"

    # Each child gets at most one gift
    for child_id, _, factory_ids in children:
        problem += lpSum(x[child_id, factory_id] for factory_id in factory_ids if (child_id, factory_id) in x) <= 1

    # Factory stock constraints
    for factory_id, (_, stock) in factory_dict.items():
        problem += lpSum(x[child_id, factory_id] for child_id, _, factory_ids in children if (child_id, factory_id) in x) <= stock

    # Country constraints
    for country_id, (max_export, min_delivery) in country_limits.items():
        country_factories = [factory_id for factory_id, (c_id, _) in factory_dict.items() if c_id == country_id]
        total_assigned = lpSum(x[child_id, factory_id] for child_id, factory_id in x if factory_id in country_factories)
        
        problem += total_assigned <= max_export  # Maximum export
        problem += total_assigned >= min_delivery  # Minimum delivery

    # Solve the problem
    status = problem.solve(PULP_CBC_CMD(msg=False))

    # Output result
    if problem.status == 1:  # Optimal
        print(int(problem.objective.value()))
    else:
        print(-1)

if __name__ == "__main__":
    solve_toy_distribution()
