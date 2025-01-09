from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpStatus
import sys

def read_input(file):
    with open(file, "r") as f:
        data = f.readlines()
    
    # First line: number of factories, countries, and children
    n, m, t = map(int, data[0].strip().split())

    # Factories
    factories = []
    for i in range(1, n + 1):
        factories.append(tuple(map(int, data[i].strip().split())))

    # Countries
    countries = []
    for i in range(n + 1, n + m + 1):
        countries.append(tuple(map(int, data[i].strip().split())))

    # Children requests
    children = []
    for i in range(n + m + 1, n + m + 1 + t):
        children.append(list(map(int, data[i].strip().split())))

    return n, m, t, factories, countries, children

def solve_toy_distribution(input_file):
    # Parse input
    n, m, t, factories, countries, children = read_input(input_file)

    # Create LP problem
    prob = LpProblem("Maximize_Satisfied_Children", LpMaximize)

    # Decision variables: x[k] = 1 if child's k-th request is fulfilled, 0 otherwise
    x = {k: LpVariable(f"x_{k}", cat="Binary") for k in range(len(children))}

    # Auxiliary variables for toy assignments to factories
    assign = {(i, k): LpVariable(f"assign_{i}_{k}", cat="Binary")
              for k in range(len(children))
              for i in range(1, n + 1)}

    # Objective: Maximize the number of satisfied children
    prob += lpSum(x[k] for k in range(len(children))), "Total_Satisfied_Children"

    # Constraint 1: A child gets at most one toy
    for k, child in enumerate(children):
        prob += lpSum(assign[i, k] for i in child[2:]) <= x[k], f"One_Toy_Per_Child_{k}"

    # Constraint 2: Factory stock limits
    factory_stock = {i: 0 for i in range(1, n + 1)}
    for factory in factories:
        i, _, f_max = factory
        factory_stock[i] = f_max

    for i in range(1, n + 1):
        prob += lpSum(assign[i, k] for k in range(len(children)) if i in children[k][2:]) <= factory_stock[i], f"Stock_Limit_{i}"

    # Constraint 3: Export limits and minimum distribution per country
    for country in countries:
        j, p_max, p_min = country
        prob += (
            lpSum(assign[i, k] for k in range(len(children)) for i in children[k][2:] if children[k][1] == j) <= p_max,
            f"Export_Limit_{j}",
        )
        prob += (
            lpSum(assign[i, k] for k in range(len(children)) for i in children[k][2:] if children[k][1] == j) >= p_min,
            f"Minimum_Distribution_{j}",
        )

    # Solve the problem
    prob.solve()

    # Check the result
    if LpStatus[prob.status] == "Optimal":
        return int(prob.objective.value())
    else:
        return -1

if __name__ == "__main__":
    # Input file should be provided as a command-line argument
    input_file = sys.argv[1]
    print(solve_toy_distribution(input_file))
