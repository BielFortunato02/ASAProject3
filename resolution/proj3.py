import sys
from pulp import *


def solve_toy_distribution(input_data):
    # Input Parsing
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read factories data
    factories = []
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        if stock:
            factories.append((factory_id, country_id, stock))

    # Read countries data
    countries = []
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries.append((country_id, max_export, min_delivery))

    # Read children data
    children = []
    for i in range(n + 1 + m, len(lines)):
        request = list(map(int, lines[i].split()))
        if request:
            children.append((request[0], request[1], request[2:]))

    # Problem Setup
    model = LpProblem(name="gift_distribution", sense=LpMaximize)

    # Decision Variables
    x = LpVariable.dicts("assign",
                         ((child, factory) for child, _, possibleRequests in children for factory in possibleRequests),
                         cat='Binary')

    # Objective Function: Maximize number of satisfied children
    model += lpSum(x[child[0], factory[0]] for child in children for factory in factories if factory[0] in child[2])

    # Constraints

    # Each child gets at most one gift
    for (child, _, possibleRequest) in children:
        model += lpSum(x[child, factory] for factory in possibleRequest) <= 1

    # Factory stock constraints
    for (factory_id, _, stock) in factories:
        model += lpSum(x[child[0], factory_id] for child in children if factory_id in child[2]) <= stock

    # Country export and delivery constraints
    for (country_id, max_export, min_delivery) in countries:
        # Maximum exports
        model += lpSum(x[child[0], factory[0]] for child in children for factory in factories
                       if factory[0] in child[2] and factory[1] == country_id and child[1] != country_id) <= max_export
        # Minimum deliveries
        model += lpSum(x[child[0], factory] for child in children for factory in child[2]
                       if child[1] == country_id) >= min_delivery

    # Solve the problem
    model.solve(GLPK_CMD(msg=1))

    # Output the result
    if model.status == 1:
        print(int(value(model.objective)))
    else:
        print(-1)


if __name__ == "__main__":
    # Read input from standard input
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)

