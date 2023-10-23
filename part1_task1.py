import os
import datetime
import argparse
import tkinter as tk
from tkinter import filedialog
from github import Github
from git import Repo
import logging

# Настройка логгера
log_filename = "github_repo_processor.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_repository(repo_url, github_token, output_folder):
    github = Github(github_token)

    # Логирование: Записываем в лог начало обработки репозитория
    logging.info(f"Processing repository: {repo_url}")

    # Папка для сохранения репозитория
    repo_info = repo_url.split('/')
    repo_owner = repo_info[-2]
    repo_name = repo_info[-1]
    repo_folder = os.path.join(output_folder, repo_name)

    if not os.path.exists(repo_folder):
        # Если папка репозитория не существует, клонируем его
        repository = github.get_repo(f"{repo_owner}/{repo_name}")
        repo = Repo.clone_from(repository.clone_url, repo_folder)
        # Логирование: Записываем в лог, что репозиторий был склонирован
        logging.info(f"Repository cloned: {repo_url}")
    else:
        # Если папка репозитория существует, открываем её
        repo = Repo(repo_folder)
        origin = repo.remotes.origin
        origin.pull()
        repository = github.get_repo(f"{repo_owner}/{repo_name}")

    # Получаем текущую дату и время 
    current_datetime = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

    # Перебираем ветки и обновляем их
    for branch in repository.get_branches():
        branch_name = branch.name
        branch_folder = os.path.join(repo_folder, branch_name)

        if not os.path.exists(branch_folder):
            # Если папка ветки не существует, создаем её и клонируем ветку
            branch_repo = Repo.clone_from(repository.clone_url, branch_folder, branch=branch_name)
            origin = branch_repo.remotes.origin
            # Логирование: Записываем в лог, что ветка была склонирована
            logging.info(f"Branch cloned: {repo_url}, branch: {branch_name}")
        else:
            # Если папка ветки существует, обновляем её
            branch_repo = Repo(branch_folder)
            origin = branch_repo.remotes.origin
            origin.pull()
            # Логирование: Записываем в лог, что ветка была обновлена
            logging.info(f"Branch updated: {repo_url}, branch: {branch_name}")

        # Создаем файл с информацией
        info_file_content = f"Repository: {repo_name}\nBranch: {branch_name}\nDate and Time: {current_datetime}"
        info_file_name = f"{repo_name}_{branch_name}_info.txt"
        info_file_path = os.path.join(branch_folder, info_file_name)

        with open(info_file_path, "w") as info_file:
            info_file.write(info_file_content)

        # Добавляем файл, делаем коммит и пушим изменения в ветку
        branch_repo.git.add(info_file_path)
        branch_repo.index.commit(f"Add {info_file_name}")
        origin.push()

        # Логирование: Записываем в лог, что информация была добавлена в ветку
        logging.info(f"Information added to branch: {repo_url}, branch: {branch_name}")

def choose_output_folder():
    root = tk.Tk()
    root.withdraw()
    output_folder = filedialog.askdirectory()
    return output_folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a list of GitHub repositories")
    parser.add_argument("github_token", type=str, help="GitHub token")
    parser.add_argument("repo_urls", nargs='+', type=str, help="List of GitHub repository URLs")

    args = parser.parse_args()

    output_folder = choose_output_folder()

    # Логирование: Записываем в лог начало выполнения программы
    logging.info("GitHub repository processing started.")

    for repo_url in args.repo_urls:
        process_repository(repo_url, args.github_token, output_folder)

    # Логирование: Записываем в лог, что программа завершила выполнение
    logging.info("GitHub repository processing completed.")