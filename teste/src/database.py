import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..//data")
DB_PATH = os.path.join(DB_DIR, "transactions.db")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS close_registers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            opening_value REAL,
            closing_value REAL,
            total_entries REAL,
            total_exits REAL,
            observations TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            note TEXT,
            date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            saldo_final REAL,
            observacao TEXT
        )
    ''')

    connection.commit()
    connection.close()

def save_close_register(date, opening_value, closing_value, total_entries, total_exits, observations):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO close_registers (date, opening_value, closing_value, total_entries, total_exits, observations)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, opening_value, closing_value, total_entries, total_exits, observations))
    connection.commit()
    connection.close()