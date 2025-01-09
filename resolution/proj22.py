import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, GLPK_CMD

def solve_toy_distribution(input_data):
    # Parse Input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read Factory Data
    factories = []
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories.append((factory_id, country_id, stock))

    # Read Country Constraints
    country_constraints = []
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        country_constraints.append((country_id, max_export, min_delivery))

    # Read Children Requests
    children = []
    for i in range(n + 1 + m, len(lines)):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        factory_ids = data[2:]
        children.append((child_id, country_id, factory_ids))

    # Initialize Problem
    problem = LpProblem("Toy_Distribution", LpMaximize)

    # Decision Variables
    x = {
        (child_id, factory_id): LpVariable(f"x_{child_id}_{factory_id}", 0, 1, cat="Binary")
        for child_id, _, factory_ids in children
        for factory_id in factory_ids
    }

    # Objective: Maximize satisfied children
    problem += lpSum(x[child_id, factory_id] for child_id, factory_id in x), "Maximize_Children"

    # Constraints

    # 1. Each child receives at most one gift
    for child_id, _, factory_ids in children:
        problem += lpSum(x[child_id, factory_id] for factory_id in factory_ids) <= 1, f"Child_{child_id}_AtMostOne"

    # 2. Factory stock constraints
    for factory_id, _, stock in factories:
        problem += lpSum(
            x[child_id, factory_id]
            for child_id, _, factory_ids in children if factory_id in factory_ids
        ) <= stock, f"Factory_{factory_id}_Stock_Limit"

    # 3. Country export and minimum delivery constraints
    for country_id, max_export, min_delivery in country_constraints:
        # Factories in this country
        country_factories = [factory_id for factory_id, c_id, _ in factories if c_id == country_id]

        # Total exports and deliveries from this country
        total_exports = lpSum(
            x[child_id, factory_id]
            for child_id, c_id, factory_ids in children
            for factory_id in factory_ids
            if factory_id in country_factories and c_id == country_id
        )

        if max_export > 0:
            problem += total_exports <= max_export, f"Country_{country_id}_Max_Export"
        if min_delivery > 0:
            problem += total_exports >= min_delivery, f"Country_{country_id}_Min_Delivery"

    # Solve Problem Using GLPK Solver
    status = problem.solve(GLPK_CMD(msg=False))

    # Output Result
    if problem.status == 1:  # Optimal Solution
        print(int(problem.objective.value()))
    else:
        print(-1)

if __name__ == "__main__":
    # Read Input from Standard Input
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)
