import random
import sys

# Generate a random integer using Gaussian distribution
def generate_random_integer(c, x):
    return int(round(random.gauss(c, x)))

# Generate a unique request for a child
def generate_request(requests, facts):
    r = int(random.uniform(1, facts))
    if requests.get(r) is None:
        requests[r] = True
        return r
    else:
        return generate_request(requests, facts)

# Generate random parameters for testing
def generate_parameters():
    num_factories = random.randint(10, 50)
    num_countries = random.randint(3, 10)
    num_children = random.randint(20, 100)
    variance = random.uniform(0.1, 0.5)
    max_cap = random.randint(50, 500)
    max_requests = random.randint(1, num_factories)

    return (num_factories, num_countries, num_children, variance, max_cap, max_requests)

# Determine test type based on size and constraints
def determine_test_type(num_factories, num_countries, num_children):
    if num_factories > 20 or num_children > 50:
        return "Stress Test"
    elif num_factories <= 3 and num_children <= 5:
        return "Basic Feasibility Test"
    elif num_factories <= 10 and num_children <= 20:
        return "Complex Scenario"
    else:
        return "Edge Case"

# Generate and save a random test case
def generate_random_test_case():
    num_factories, num_countries, num_children, variance, max_cap, max_requests = generate_parameters()

    fs_per_country = []
    cs_per_country = []

    avg_fs_per_country = int(num_factories / num_countries)
    avg_cs_per_country = int(num_children / num_countries)

    total_fs = 0
    total_cs = 0

    factories_data = {}
    countries_data = {}
    children_data = {}

    countries_info = []
    cur_fact = 1
    cur_child = 1

    for c in range(num_countries):
        cur_fs = generate_random_integer(avg_fs_per_country, avg_fs_per_country * variance)
        cur_cs = generate_random_integer(avg_cs_per_country, avg_cs_per_country * variance)

        if (num_factories - total_fs < cur_fs or c == (num_countries - 1)):
            cur_fs = num_factories - total_fs

        if (num_children - total_cs < cur_cs or c == (num_countries - 1)):
            cur_cs = num_children - total_cs

        countries_info.append((cur_fs, cur_cs))
        total_fs += cur_fs
        total_cs += cur_cs

        cur_total_cap = 0
        for j in range(cur_fact, total_fs + 1):
            cap = int(random.uniform(1, max_cap))
            cur_total_cap += cap
            factories_data[j] = (j, c + 1, cap)

        country_export_cap = int(random.uniform(cur_total_cap / 4, cur_total_cap))
        country_min_cs = int(random.uniform(cur_cs / 4, cur_cs))
        countries_data[c + 1] = (c + 1, country_export_cap, country_min_cs)

        for ch in range(cur_child, total_cs + 1):
            requests_num = int(random.uniform(1, max_requests))
            assert (requests_num < num_factories)
            lst = [ch, c + 1]
            requests = {}
            for i in range(requests_num):
                r = generate_request(requests, num_factories)
                lst.append(r)
            children_data[ch] = lst

        cur_fact = total_fs + 1
        cur_child = total_cs + 1

    # Determine test type
    test_type = determine_test_type(num_factories, num_countries, num_children)

    # Save the test case to a file
    with open("testfile", "w") as f:
        f.write(f"{num_factories} {num_countries} {num_children}\n")
        for i in range(num_factories):
            fi, pj, fmaxi = factories_data[i + 1]
            f.write(f"{fi} {pj} {fmaxi}\n")
        for i in range(num_countries):
            pj, pmaxj, pminj = countries_data[i + 1]
            f.write(f"{pj} {pmaxj} {pminj}\n")
        for i in range(num_children):
            c_data = children_data[i + 1]
            f.write(" ".join(map(str, c_data)) + "\n")

    print(f"Test Type: {test_type}")
    print("Test case saved to 'testfile'")

if __name__ == "__main__":
    generate_random_test_case()
