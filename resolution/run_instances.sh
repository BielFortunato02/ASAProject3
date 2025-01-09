#!/bin/bash

# Diretório de entrada com os arquivos gerados pelo p3_gerador.py
INPUT_DIR="inputs"
OUTPUT_CSV="final_results.csv"

# Cabeçalho do CSV final
echo "Instance,NumFactories,NumCountries,NumChildren,NumVariables,NumRestrictions,ExecutionTime" > $OUTPUT_CSV

# Iterar sobre todos os arquivos no diretório de entrada
for input_file in "$INPUT_DIR"/*.txt; do
    # Nome da instância (sem diretório e extensão)
    instance_name=$(basename "$input_file" .txt)

    # Executar o proj23.py com o arquivo de entrada
    start_time=$(date +%s.%N)
    output=$(python3 proj23.py < "$input_file")
    end_time=$(date +%s.%N)

    # Calcular tempo de execução
    execution_time=$(echo "$end_time - $start_time" | bc)

    # Extrair informações do arquivo de entrada
    num_factories=$(head -n 1 "$input_file" | awk '{print $1}')
    num_countries=$(head -n 1 "$input_file" | awk '{print $2}')
    num_children=$(grep -c "^" "$input_file") # Contar o número de linhas

    # Número de variáveis e restrições (simulação no exemplo)
    num_variables=$((num_factories + num_children))
    num_restrictions=$((num_factories + num_countries + num_children))

    # Salvar os resultados no CSV
    echo "$instance_name,$num_factories,$num_countries,$num_children,$num_variables,$num_restrictions,$execution_time" >> $OUTPUT_CSV

    echo "Processado: $input_file -> Tempo: $execution_time s"
done
