import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD


def solve_toy_distribution(input_data):
    # Parse Input
    lines = input_data.strip().split("\n")
    n, m, t = map(int, lines[0].split())

    # Read Factory Data
    factories = []
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories.append((factory_id, country_id, stock))

    # Read Country Data
    countries = []
    for i in range(n + 1, n + 1 + m):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries.append((country_id, max_export, min_delivery))

    # Read Children's Requests
    children = []
    for i in range(n + 1 + m, len(lines)):
        request = list(map(int, lines[i].split()))
        children.append((request[0], request[1], request[2:]))

    # Linear Programming Model
    model = LpProblem(name="gift_distribution", sense=LpMaximize)

    # Decision Variables
    x = LpVariable.dicts("x", ((k, i) for k, _, factories_list in children for i in factories_list), cat='Binary')

    # Objective Function: Maximize satisfied children
    model += lpSum(x[k, i] for k, _, factories_list in children for i in factories_list)

    # Constraints

    # Each child gets at most one gift
    for k, _, factories_list in children:
        model += lpSum(x[k, i] for i in factories_list) <= 1

    # Factory capacity constraints
    for i, _, stock in factories:
        model += lpSum(x[k, i] for k, _, factories_list in children if i in factories_list) <= stock

    # Country export and minimum delivery constraints
    for j, pmax, pmin in countries:
        # Maximum exports
        model += lpSum(x[k, i] for k, _, factories_list in children 
                       for i in factories_list if any(f[0] == i and f[1] == j for f in factories)) <= pmax
        # Minimum deliveries
        model += lpSum(x[k, i] for k, _, factories_list in children 
                       for i in factories_list if any(f[0] == i and f[1] == j for f in factories)) >= pmin

    # Solve the Model
    model.solve(PULP_CBC_CMD(msg=False))

    # Output Result
    if LpStatus[model.status] == 'Optimal':
        print(sum(1 for k, _, factories_list in children for i in factories_list if x[k, i].varValue == 1))
    else:
        print(-1)


if __name__ == "__main__":
    # Read input from stdin
    input_data = sys.stdin.read()
    solve_toy_distribution(input_data)


'''
Hint:

T06

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
