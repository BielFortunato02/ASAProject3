import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

def main():
    # Parse input
    input_data = sys.stdin.read().splitlines()
    
    # Read the first line
    n, m, t = map(int, input_data[0].split())

    # Validate input length
    expected_lines = 1 + n + m + t
    if len(input_data) < expected_lines:
        raise ValueError("Input data is incomplete or inconsistent with n, m, and t values.")

    # Read factory data
    factories = []
    for i in range(1, 1 + n):
        factory_id, country_id, stock = map(int, input_data[i].split())
        factories.append((factory_id, country_id, stock))

    # Read country constraints
    country_constraints = []
    for i in range(1 + n, 1 + n + m):
        country_id, pmax, pmin = map(int, input_data[i].split())
        country_constraints.append((country_id, pmax, pmin))

    # Read child requests
    children = []
    for i in range(1 + n + m, 1 + n + m + t):
        request = list(map(int, input_data[i].split()))
        child_id, country_id, factories_list = request[0], request[1], request[2:]
        children.append((child_id, country_id, factories_list))

    # Rest of the code remains unchanged


    # Define the problem
    problem = LpProblem("Maximize_Children_Satisfied", LpMaximize)

    # Create decision variables
    # x[k][i] = 1 if child k gets a gift from factory i, 0 otherwise
    x = {
        (child_id, factory_id): LpVariable(f"x_{child_id}_{factory_id}", 0, 1, cat="Binary")
        for child_id, _, factories_list in children
        for factory_id in factories_list
    }

    # Objective function: Maximize the number of satisfied children
    problem += lpSum(x[child_id, factory_id] for child_id, factory_id in x), "Total_Satisfied_Children"

    # Constraint 1: Each child can receive at most one gift
    for child_id, _, factories_list in children:
        problem += lpSum(x[child_id, factory_id] for factory_id in factories_list) <= 1, f"Child_{child_id}_One_Gift"

    # Constraint 2: Factory production limits
    for factory_id, _, stock in factories:
        problem += lpSum(
            x[child_id, factory_id] for child_id, _, factories_list in children if factory_id in factories_list
        ) <= stock, f"Factory_{factory_id}_Stock_Limit"

    # Constraint 3: Country export limits
    for country_id, pmax, pmin in country_constraints:
        # Total exports from this country
        country_factories = [factory_id for factory_id, c_id, _ in factories if c_id == country_id]
        
        total_exports = lpSum(
            x[child_id, factory_id]
            for child_id, c_id, factories_list in children
            for factory_id in factories_list
            if factory_id in country_factories and c_id == country_id
        )
        
        problem += total_exports <= pmax, f"Country_{country_id}_Max_Export"
        problem += total_exports >= pmin, f"Country_{country_id}_Min_Distribution"

    # Solve the problem
    status = problem.solve(PULP_CBC_CMD(msg=False))

    # Output the result
    if problem.status == 1:  # Optimal
        print(int(problem.objective.value()))
    else:
        print(-1)

if __name__ == "__main__":
    main()
