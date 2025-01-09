import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PulpSolverError

def main():
    # Read input
    input_data = sys.stdin.read().strip().splitlines()
    n, m, t = map(int, input_data[0].split())

    # Factories
    factories = []
    for i in range(1, n + 1):
        f_id, country_id, stock = map(int, input_data[i].split())
        factories.append((f_id, country_id, stock))

    # Countries
    countries = []
    offset = n + 1
    for j in range(offset, offset + m):
        c_id, max_export, min_delivery = map(int, input_data[j].split())
        countries.append((c_id, max_export, min_delivery))

    # Requests
    requests = []
    offset += m
    for k in range(offset, offset + t):
        data = list(map(int, input_data[k].split()))
        child_id = data[0]
        country_id = data[1]
        factory_ids = data[2:]
        requests.append((child_id, country_id, factory_ids))

    # Create problem
    prob = LpProblem("Maximize_Satisfied_Requests", LpMaximize)

    # Variables
    x = {}
    for c in range(t):
        for f in requests[c][2]:  # Factories in the request
            x[c, f] = LpVariable(f"x_{c}_{f}", 0, 1, cat="Binary")

    # Objective Function
    prob += lpSum(x[c, f] for c in range(t) for f in requests[c][2]), "Maximize Requests"

    # Constraints
    # 1. Each child can get at most one toy
    for c in range(t):
        prob += lpSum(x[c, f] for f in requests[c][2]) <= 1, f"Child_One_Toy_{c}"

    # 2. Factory stock limits
    for f_id, _, stock in factories:
        prob += lpSum(x[c, f_id] for c in range(t) if f_id in requests[c][2]) <= stock, f"Factory_Stock_{f_id}"

    # 3. Export limits by country
    for c_id, max_export, _ in countries:
        prob += (
            lpSum(
                x[c, f] for c in range(t) for f in requests[c][2]
                if any(f == f_id and country_id == c_id for f_id, country_id, _ in factories)
            ) <= max_export,
            f"Country_Export_Limit_{c_id}"
        )

    # 4. Minimum delivery by country
    for c_id, _, min_delivery in countries:
        prob += (
            lpSum(
                x[c, f] for c in range(t) for f in requests[c][2]
                if any(f == f_id and country_id == c_id for f_id, country_id, _ in factories)
            ) >= min_delivery,
            f"Country_Minimum_Delivery_{c_id}"
        )

    # Solve the problem
    try:
        prob.solve()
    except PulpSolverError:
        print(-1)
        return

    # Output results
    if prob.status != 1:  # Status 1 means Optimal
        print(-1)
    else:
        print(int(prob.objective.value()))


if __name__ == "__main__":
    main()
