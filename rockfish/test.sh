# Populating my_array
IFS=$'\n' read -d '' -r -a tasks < ../data/splits/evaluation_tasks_easy.txt

# Iterate over the array and print each string
for line in "${tasks[@]}"; do
    echo "$line"
done
