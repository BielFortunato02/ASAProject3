import sys
from pulp import *


def solve_toy_distribution(input_data):
    # Input Parsing
    lines = input_data.strip().split("\n")
    n, m = map(int, lines[0].split())

    # Parse factories
    factories = {int(line.split()[0]): {"country_id": int(line.split()[1]), "stock": int(line.split()[2])}
                 for line in lines[1:n + 1]}

    # Parse countries
    countries = {int(line.split()[0]): {"max_export": int(line.split()[1]), "min_delivery": int(line.split()[2])}
                 for line in lines[n + 1:n + 1 + m]}

    # Parse children
    children = [{"id": int(line.split()[0]), "country_id": int(line.split()[1]), "requests": list(map(int, line.split()[2:]))}
                for line in lines[n + 1 + m:]]

    # Eliminate unnecessary data iteratively
    while True:
        # Filter factories with stock > 0 and requested by at least one child
        requested_factories = set(factory_id for child in children for factory_id in child["requests"])
        factories = {factory_id: details for factory_id, details in factories.items()
                     if factory_id in requested_factories and details["stock"] > 0}

        # Filter children that can request from at least one remaining factory
        children = [child for child in children if any(factory_id in factories for factory_id in child["requests"])]

        # Filter countries connected to active children or factories
        relevant_countries = set(child["country_id"] for child in children).union(
            factory["country_id"] for factory in factories.values())
        countries = {country_id: details for country_id, details in countries.items()
                     if country_id in relevant_countries}

        # Check if pruning is complete (no further changes)
        if not requested_factories - factories.keys():
            break

    # Problem Setup
    model = LpProblem(name="gift_distribution", sense=LpMaximize)

    # Decision Variables
    x = LpVariable.dicts("assign",
                         [(child["id"], factory_id) for child in children for factory_id in child["requests"]
                          if factory_id in factories],
                         cat='Binary')

    # Objective Function: Maximize number of satisfied children
    model += lpSum(x[child["id"], factory_id] for child in children for factory_id in child["requests"]
                   if factory_id in factories)

    # Constraints
    # Each child gets at most one gift
    for child in children:
        model += lpSum(x[child["id"], factory_id] for factory_id in child["requests"] if factory_id in factories) <= 1

    # Factory stock constraints
    for factory_id, factory in factories.items():
        model += lpSum(x[child["id"], factory_id] for child in children if factory_id in child["requests"]) <= factory["stock"]

    # Country export and delivery constraints
    for country_id, country in countries.items():
        # Maximum exports
        model += lpSum(x[child["id"], factory_id] for child in children for factory_id in child["requests"]
                       if factory_id in factories and factories[factory_id]["country_id"] == country_id and child["country_id"] != country_id) <= country["max_export"]
        # Minimum deliveries
        model += lpSum(x[child["id"], factory_id] for child in children for factory_id in child["requests"]
                       if factory_id in factories and child["country_id"] == country_id) >= country["min_delivery"]

    # Solve the problem
    model.solve(GLPK_CMD(msg=0))

    # Output the result
    print(int(value(model.objective)) if model.status == 1 else -1)


if __name__ == "__main__":
    # Read input from standard input
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)
