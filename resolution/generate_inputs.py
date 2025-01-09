import csv
import random

def create_input_files(csv_file, output_dir):
    """
    Lê os dados do arquivo CSV e cria arquivos de entrada para o proj23.py
    """
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Iterar sobre cada linha do CSV e criar um arquivo de entrada
        for i, row in enumerate(reader):
            num_factories = int(row['num_factories'])
            num_countries = int(row['num_countries'])
            num_children = int(row['num_children'])

            # Criação dos dados no formato esperado
            factories = []
            countries = []
            children = []

            # Gerar dados das fábricas
            for factory_id in range(1, num_factories + 1):
                country_id = random.randint(1, num_countries)  # Associar fábrica a um país aleatório
                stock = random.randint(10, 1000)  # Capacidade de produção aleatória
                factories.append((factory_id, country_id, stock))

            # Gerar dados dos países
            for country_id in range(1, num_countries + 1):
                max_export = random.randint(100, 500)  # Exportação máxima
                min_delivery = random.randint(10, 100)  # Entrega mínima
                countries.append((country_id, max_export, min_delivery))

            # Gerar dados das crianças
            for child_id in range(1, num_children + 1):
                country_id = random.randint(1, num_countries)  # País da criança
                num_requests = random.randint(1, min(5, num_factories))  # Número de fábricas pedidas
                requests = random.sample(range(1, num_factories + 1), num_requests)  # Fábricas aleatórias
                children.append((child_id, country_id, requests))

            # Criar o arquivo de entrada
            output_file = f"{output_dir}/input_instance_{i+1}.txt"
            with open(output_file, 'w') as out:
                # Linha 1: Número de fábricas e países
                out.write(f"{num_factories} {num_countries}\n")
                
                # Linhas das fábricas
                for factory in factories:
                    out.write(f"{factory[0]} {factory[1]} {factory[2]}\n")

                # Linhas dos países
                for country in countries:
                    out.write(f"{country[0]} {country[1]} {country[2]}\n")

                # Linhas das crianças
                for child in children:
                    out.write(f"{child[0]} {child[1]} {' '.join(map(str, child[2]))}\n")

            print(f"Arquivo criado: {output_file}")

# Use o script com os seguintes parâmetros
csv_file = "experiment_results.csv"  # Nome do arquivo gerado pelo p3_gerador.py
output_dir = "./inputs"  # Diretório para salvar os arquivos de entrada

# Criar o diretório, se necessário
import os
os.makedirs(output_dir, exist_ok=True)

# Executar a função
create_input_files(csv_file, output_dir)
