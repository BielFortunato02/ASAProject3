import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

def solve_toy_distribution(input_data):
    # Parse input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Factories data
    factories = []
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories.append((factory_id, country_id, stock))

    # Country constraints
    country_constraints = []
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        country_constraints.append((country_id, max_export, min_delivery))

    # Children requests
    children = []
    for i in range(n + 1 + m, len(lines)):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        factory_ids = data[2:]
        children.append((child_id, country_id, factory_ids))

    # Initialize the problem
    problem = LpProblem("Toy_Distribution", LpMaximize)

    # Decision variables
    x = {
        (child_id, factory_id): LpVariable(f"x_{child_id}_{factory_id}", 0, 1, cat="Binary")
        for child_id, _, factories_list in children
        for factory_id in factories_list
    }

    # Objective: Maximize the number of satisfied children
    problem += lpSum(x[child_id, factory_id] for child_id, factory_id in x), "Maximize_Children"

    # Constraint: Each child receives at most one gift
    for child_id, _, factories_list in children:
        problem += lpSum(x[child_id, factory_id] for factory_id in factories_list) <= 1, f"Child_{child_id}_AtMostOne"

    # Constraint: Factory production limits
    for factory_id, _, stock in factories:
        problem += lpSum(
            x[child_id, factory_id]
            for child_id, _, factories_list in children if factory_id in factories_list
        ) <= stock, f"Factory_{factory_id}_Stock_Limit"

    # Constraints: Country export limits and minimum distributions
    for country_id, max_export, min_delivery in country_constraints:
        # Factories in this country
        country_factories = [factory_id for factory_id, c_id, _ in factories if c_id == country_id]
        
        # Total assignments to children in this country
        country_assignments = lpSum(
            x[child_id, factory_id]
            for child_id, c_id, factories_list in children
            for factory_id in factories_list
            if factory_id in country_factories and c_id == country_id
        )

        problem += country_assignments <= max_export, f"Country_{country_id}_Max_Export"
        problem += country_assignments >= min_delivery, f"Country_{country_id}_Min_Delivery"

    # Solve the problem
    status = problem.solve(PULP_CBC_CMD(msg=False))

    # Output the result
    if problem.status == 1:  # Optimal
        print(int(problem.objective.value()))
    else:
        print(-1)

if __name__ == "__main__":
    # Read input from stdin
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)
