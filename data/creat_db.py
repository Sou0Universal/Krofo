import sqlite3
import os

# Caminho para a pasta 'data'
DB_PATH = os.path.join(os.getcwd(), "data", "transactions.db")

def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS close_registers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            closing_value REAL,
            observations TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            saldo_inicial REAL,
            total_entradas REAL,
            total_saidas REAL,
            saldo_final REAL,
            observacao TEXT
        )
    ''')
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    # Verificar se a pasta 'data' existe, se não, criar
    if not os.path.exists(os.path.join(os.getcwd(), "data")):
        os.makedirs(os.path.join(os.getcwd(), "data"))
    
    # Remover o arquivo de banco de dados antigo se ele existir
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    create_database()
    print("Banco de dados criado com sucesso na pasta 'data'.")