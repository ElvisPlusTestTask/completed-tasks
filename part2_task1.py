import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog

def check_and_add_messages(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT user FROM data')
    users = [row[0] for row in cursor.fetchall()]

    # Проверяем для каждого пользователя есть ли уже для него запись
    for user in users:
        cursor.execute('SELECT * FROM messages WHERE user = ?', (user,))
        existing_message = cursor.fetchone()

        if existing_message:
            print(f'Для {user} уже существует запись в таблице.')
            continue

        # Получаем записи пользователя
        cursor.execute('SELECT datastr FROM data WHERE user = ?', (user,))
        user_entries = [row[0] for row in cursor.fetchall()]

        # Создаем список дат, которые должны быть в записях пользователя и преобразуем их в даты без времени
        target_dates = [(datetime.now().date() - timedelta(days=day)).strftime('%Y%m%d') for day in range(7)]
        user_entry_dates = [entry[:8] for entry in user_entries]

        # Проверяем наличие записей для каждого дня недели и добавляем сообщение во вторую таблицу
        has_entries_for_every_day = all(target_date in user_entry_dates for target_date in target_dates)

        if has_entries_for_every_day:
            message = 'есть запись'
            cursor.execute('INSERT INTO messages (user, message) VALUES (?, ?)', (user, message))
            print(f'Для {user} добавлено сообщение в таблицу: {message}')
        else:
            print(f'Нет записей для {user} в течение недели.')
            print(f'Записи пользователя {user}: {user_entries}')

        # Удаление некорректных записей
        for entry in user_entries:
            if not is_valid_entry(entry):
                cursor.execute('DELETE FROM data WHERE datastr = ?', (entry,))
                print(f'Некорректная запись удалена: {entry}')

    conn.commit()
    conn.close()

def is_valid_entry(entry):
    try:
        date_obj = datetime.strptime(entry, '%Y%m%d%H%M%S')
        is_valid = (1 <= date_obj.month <= 12) and (1 <= date_obj.day <= 31) and (0 <= date_obj.hour <= 23) and (0 <= date_obj.minute <= 59) and (0 <= date_obj.second <= 59)
        return is_valid
    except ValueError:
        return False

def choose_database_file():
    root = tk.Tk()
    root.withdraw()
    database_path = filedialog.askopenfilename(filetypes=[("SQLite databases", "*.db")])
    return database_path

if __name__ == '__main__':
    database_path = choose_database_file()
    check_and_add_messages(database_path)
