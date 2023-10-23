#!/bin/bash

# Настройка логгирования
LOG_FILE="task2.log"
exec > >(tee -a "$LOG_FILE") 2>&1

process_repository() {
    repo_url="$1"
    github_token="$2"
    output_folder="$3"

    echo "Processing repository: $repo_url"

    # Извлекаем имя владельца и имя репозитория из URL
    IFS='/' read -ra repo_info <<< "$repo_url"
    repo_owner="${repo_info[-2]}"
    repo_name="${repo_info[-1]}"
    repo_folder="$output_folder/$repo_name"

    if [ ! -d "$repo_folder" ]; then
        # Если папка репозитория не существует, клонируем его
        git clone "https://$github_token@github.com/$repo_owner/$repo_name.git" "$repo_folder"
    else
        # Если папка репозитория существует, обновляем её
        cd "$repo_folder" || exit
        git pull
    fi

    # Получаем текущую дату и время 
    current_datetime=$(date +"%d.%m.%Y - %H:%M:%S")

    # Перебираем ветки и обновляем их
    branches=$(git ls-remote --heads "https://github.com/$repo_owner/$repo_name.git" | awk -F'/' '{print $3}')
    for branch in $branches; do
        branch_folder="$repo_folder/$branch"

        echo "Processing branch: $branch"

        if [ ! -d "$branch_folder" ]; then
            # Если папка ветки не существует, создаем её и клонируем ветку
            git clone --single-branch --branch "$branch" "https://$github_token@github.com/$repo_owner/$repo_name.git" "$branch_folder"
        else
            # Если папка ветки существует, обновляем её
            cd "$branch_folder" || exit
            git pull
        fi

        # Создаем файл с информацией
        info_file_content="Repository: $repo_name\nBranch: $branch\nDate and Time: $current_datetime"
        info_file_name="${repo_name}_${branch}_info.txt"
        info_file_path="$branch_folder/$info_file_name"

        echo -e "$info_file_content" > "$info_file_path"

        # Добавляем файл, делаем коммит и пушим изменения в ветку
        git add "$info_file_path"
        git commit -m "Add $info_file_name"
        git push
    done
}

echo "Введите путь к папке вывода:"
read output_folder

github_token="$1"
shift
repo_urls=("$@")

for repo_url in "${repo_urls[@]}"; do
    process_repository "$repo_url" "$github_token" "$output_folder"
done