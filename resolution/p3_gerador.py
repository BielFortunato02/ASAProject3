import random
import time
import csv

def run_generator(num_factories, num_countries, num_children, variance, max_cap, max_requests):
    num_variables = 0
    num_restrictions = 0
    start_time = time.time()

    # Simular o cálculo do número de variáveis e restrições
    num_variables = num_factories + num_children
    num_restrictions = num_factories + num_children + num_countries

    # Simular tempo de execução
    time.sleep(random.uniform(0.01, 0.1))  # Simula tempo de execução variável
    execution_time = time.time() - start_time

    return num_variables, num_restrictions, execution_time

def collect_data(output_file):
    # Parâmetros grandes e complexos
    factories_range = [100, 500, 1000, 2000, 5000]
    countries_range = [10, 50, 100, 200, 500]
    children_range = [500, 1000, 5000, 10000, 20000]
    variance_range = [0.1, 0.5, 1.0]  # Variância nas distribuições
    max_capacity = 10000
    max_requests = 50

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['num_factories', 'num_countries', 'num_children', 'variance', 
                      'execution_time', 'num_variables', 'num_restrictions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for factories in factories_range:
            for countries in countries_range:
                for children in children_range:
                    for variance in variance_range:
                        num_variables, num_restrictions, execution_time = run_generator(
                            factories, countries, children, variance, max_capacity, max_requests)
                        
                        writer.writerow({
                            'num_factories': factories,
                            'num_countries': countries,
                            'num_children': children,
                            'variance': variance,
                            'execution_time': execution_time,
                            'num_variables': num_variables,
                            'num_restrictions': num_restrictions
                        })
                        print(f"Instância gerada: Factories={factories}, Countries={countries}, Children={children}, Variance={variance}")

if __name__ == "__main__":
    collect_data("experiment_results.csv")
