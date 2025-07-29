#!/bin/bash

echo -e "\033[0;36mTest de balanceo de carga para el endpoint /instancia\033[0m"
echo -e "\033[0;36m--------------------------------------------------------\033[0m"

declare -A conteo

for i in {1..10}; do
    respuesta=$(curl -s http://localhost:8000/api/instancia)
    instancia=$(echo "$respuesta" | jq -r '.instancia')

    if [[ "$instancia" == "null" || -z "$instancia" ]]; then
        echo -e "\033[0;31mError en la petición $i\033[0m"
    else
        ((conteo["$instancia"]++))
        echo -e "\033[0;32mPetición $i -> Respondió: $instancia\033[0m"
    fi

    sleep 0.5
done

echo -e "\n\033[1;33mResumen de respuestas:\033[0m"
for key in "${!conteo[@]}"; do
    echo -e "\033[0;37m$key: ${conteo[$key]} respuestas\033[0m"
done
