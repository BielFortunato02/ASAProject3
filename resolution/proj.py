import pulp
import sys

def solve_toy_distribution(input_data):

    # Parse the input data
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    factories = []
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories.append((factory_id, country_id, stock))

    countries = []
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries.append((country_id, max_export, min_delivery))

    children = []
    for i in range(n + 1 + m, len(lines)):
        child_request = list(map(int, lines[i].split()))
        children.append((child_request[0], child_request[1], child_request[2:]))

    # Create a linear programming problem
    prob = pulp.LpProblem("Maximize_Toys_Distribution", pulp.LpMaximize)

    # Decision variables
    x = pulp.LpVariable.dicts("assign", ((child[0], factory) for child in children for factory in child[2]), 
                              cat=pulp.LpBinary)

    # Objective function: Maximize the number of children satisfied
    prob += pulp.lpSum(x[child[0], factory] for child in children for factory in child[2])

    # Constraints
    # Each child gets at most one toy
    for child in children:
        prob += pulp.lpSum(x[child[0], factory] for factory in child[2]) <= 1

    # Factories' stock limits
    for factory_id, _, stock in factories:
        prob += pulp.lpSum(x[child[0], factory_id] for child in children if factory_id in child[2]) <= stock

    # Countries' export and minimum delivery constraints
    for country_id, max_export, min_delivery in countries:
        prob += pulp.lpSum(x[child[0], factory] for child in children for factory in child[2]
                           if any(f[0] == factory and f[1] == country_id for f in factories)) <= max_export
        prob += pulp.lpSum(x[child[0], factory] for child in children for factory in child[2]
                           if any(f[0] == factory and f[1] == country_id for f in factories)) >= min_delivery

    # Solve the problem with logs disabled
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Check the status and return results
    if pulp.LpStatus[prob.status] != "Optimal":
        return print(-1)

    return print(int(pulp.value(prob.objective)))

if __name__ == "__main__":
    # Lê os dados do stdin
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)


'''
Hint:

T05

2 tests with Time Limit Exceeded 16 tests with Accepted 16 tests with Wrong Answer 2 tests with Time Limit ExceededObservation of Time Limit Exceeded

(test T06): Time Limit Exceeded
(test T07): OK
(test T08): OK
(test T09): OK
(test T10): OK
(test T11): Wrong Answer
(test T12): OK
(test T13): Wrong Answer
(test T14): Wrong Answer
(test T15): Wrong Answer
(test T16): OK
(test T17): OK
(test T18): OK
(test T19): OK
(test T20): Wrong Answer
(test T21): Wrong Answer
(test T22): Wrong Answer
(test T23): Wrong Answer
(test T24): Wrong Answer
(test T25): Wrong Answer
(test T26): OK
(test T27): OK
(test T28): OK
(test T29): Wrong Answer
(test T30): Wrong Answer
(test T31): Time Limit Exceeded
'''