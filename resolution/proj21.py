import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD


def solve_toy_distribution(input_data):
    # Parse input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read factories data
    factories = {factory_id: (country_id, stock) for factory_id, country_id, stock in
                 (map(int, lines[i].split()) for i in range(1, n + 1))}

    # Read countries data
    countries = {country_id: (max_export, min_delivery) for country_id, max_export, min_delivery in
                 (map(int, lines[i].split()) for i in range(n + 1, n + 1 + m))}

    # Read children requests
    children = [(request[0], request[1], request[2:]) for request in
                (list(map(int, lines[i].split())) for i in range(n + 1 + m, len(lines)))]

    # Initialize the optimization problem
    model = LpProblem(name="Toy_Distribution", sense=LpMaximize)

    # Decision Variables
    x = {
        (child_id, factory_id): LpVariable(f"x_{child_id}_{factory_id}", cat="Binary")
        for child_id, _, factories_list in children
        for factory_id in factories_list if factory_id in factories
    }

    # Objective Function: Maximize the number of satisfied children
    model += lpSum(x.values()), "Maximize_Satisfied_Children"

    # Constraints

    # Each child receives at most one gift
    for child_id, _, factories_list in children:
        model += lpSum(x[child_id, factory_id] for factory_id in factories_list if (child_id, factory_id) in x) <= 1, \
                 f"Child_{child_id}_One_Gift"

    # Factory stock constraints
    for factory_id, (_, stock) in factories.items():
        model += lpSum(x[child_id, factory_id] for child_id, _, factories_list in children
                       if (child_id, factory_id) in x) <= stock, f"Factory_{factory_id}_Stock_Limit"

    # Country constraints: Maximum exports and minimum deliveries
    for country_id, (max_export, min_delivery) in countries.items():
        # Factories in the country
        country_factories = [factory_id for factory_id, (c_id, _) in factories.items() if c_id == country_id]

        # Total assignments to children in the country
        country_assignments = lpSum(x[child_id, factory_id] for child_id, _, factories_list in children
                                    for factory_id in factories_list if factory_id in country_factories and
                                    (child_id, factory_id) in x)

        model += country_assignments <= max_export, f"Country_{country_id}_Max_Export"
        model += country_assignments >= min_delivery, f"Country_{country_id}_Min_Delivery"

    # Solve the problem with a time limit to avoid memory issues
    model.solve(PULP_CBC_CMD(msg=False, timeLimit=30))

    # Output the result
    if LpStatus[model.status] == "Optimal":
        result = int(sum(x[child_id, factory_id].varValue for child_id, factory_id in x if x[child_id, factory_id].varValue))
        print(result)
    else:
        print(-1)


if __name__ == "__main__":
    # Read input from standard input
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)
