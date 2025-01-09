import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, PULP_CBC_CMD

# Input Parsing
n, m, t = map(int, input().split())

factories = []
for _ in range(n):
    i, j, stock = map(int, input().split())
    factories.append((i, j, stock))

countries = []
for _ in range(m):
    j, pmax, pmin = map(int, input().split())
    countries.append((j, pmax, pmin))

children = []
for _ in range(t):
    request = list(map(int, input().split()))
    children.append(request)

# Problem Setup
model = LpProblem(name="gift_distribution", sense=LpMaximize)

# Decision Variables
x = [[LpVariable(f"x_{k}_{i}", cat='Binary') for i in range(1, n + 1)] for k in range(1, t + 1)]

# Objective Function: Maximize number of satisfied children
model += lpSum(x[k-1][i-1] for k in range(1, t + 1) for i in range(1, n + 1))

# Constraints

# Each child gets at most one gift
for k in range(t):
    model += lpSum(x[k][i] for i in range(n)) <= 1

# Factory capacity constraints
for i in range(n):
    factory_id, country_id, stock = factories[i]
    model += lpSum(x[k][i] for k in range(t) if (i+1) in children[k][2:]) <= stock

# Country export and minimum delivery constraints
for j in range(m):
    pmax, pmin = countries[j][1], countries[j][2]
    
    # Maximum exports
    model += lpSum(x[k][i] for k in range(t) for i in range(n) if factories[i][1] == j + 1) <= pmax

    # Minimum deliveries
    model += lpSum(x[k][i] for k in range(t) for i in range(n) if factories[i][1] == j + 1) >= pmin

# Solve the problem
model.solve(PULP_CBC_CMD(msg=False))

# Output result
if LpStatus[model.status] == 'Optimal':
    result = int(sum(x[k][i].varValue for k in range(t) for i in range(n)))
    print(result)
else:
    print(-1)


'''
Hint:

T03

1 test with Memory Limit Exceeded 9 tests with Time Limit Exceeded 11 tests with Accepted 13 tests with Wrong Answer 9 tests with Time Limit ExceededObservation of Time Limit Exceeded

(test T26): Time Limit Exceeded
(test T27): Time Limit Exceeded
(test T28): Time Limit Exceeded
(test T29): Real timeout exceeded
(tried to read past end of file?)
(test T30): Time Limit Exceeded
(test T31): Time Limit Exceeded
(test T32): Time Limit Exceeded
(test T33): Time Limit Exceeded
(test T34): Time Limit Exceeded
'''