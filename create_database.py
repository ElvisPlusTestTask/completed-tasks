#create_database.py

import sqlite3
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta

def create_tables(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            user TEXT,
            datastr TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            user TEXT,
            message TEXT
        )
    ''')

    # Добавляем записи в первую таблицу
    today = datetime.now()
    records_data = [
        ('user1', (today - timedelta(days=day)).strftime('%Y%m%d%H%M%S')) for day in range(7)
    ]
    records_data.extend([
        ('user2', (today - timedelta(days=0)).strftime('%Y%m%d%H%M%S')),
        ('user3', (today - timedelta(days=1)).strftime('%Y%m%d%H%M%S')),
        ('user4', '20231024130724'),
        ('user4', '20231023130724'),
        ('user4', '20231022130724'),
        ('user4', '20231021130724'),
        ('user4', '20231020130724'),
        ('user4', '20231019130724'),
        ('user4', '20231018130724'),
        ('user5', '20231031130724'),
        ('user5', '20231032130724'),
        ('user5', '20231033130724'),
        ('user5', '20231034130724'),
        ('user5', '20231035130724'),
        ('user5', '20231036130724'),
        ('user5', '20231037130724'),

    ])
    cursor.executemany('INSERT INTO data (user, datastr) VALUES (?, ?)', records_data)
    
    conn.commit()
    conn.close()

def choose_database_file():
    root = tk.Tk()
    root.withdraw()
    database_path = filedialog.asksaveasfilename(defaultextension=".db .sqlite", filetypes=[("SQLite databases", "*.db *.sqlite")])
    return database_path

if __name__ == '__main__':
    database_path = choose_database_file()
    create_tables(database_path)
