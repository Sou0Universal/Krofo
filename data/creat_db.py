import sqlite3

# Caminhos para os bancos de dados antigos
db_paths = {
    'clientes': 'clientes.db',
    'pagamentos': 'pagamentos.db',
    'produtos': 'produtos.db',
    'transactions': 'transactions.db',
    'users': 'users.db'
}

# Novo banco de dados
new_db_path = 'sistema.bd'

def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def migrate_data():
    # Conectar ao novo banco de dados
    new_connection = sqlite3.connect(new_db_path)
    new_cursor = new_connection.cursor()

    # Criar tabelas no novo banco de dados
    new_cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            code TEXT,
            category TEXT,
            description TEXT,
            sale_price REAL,
            cost_price REAL,
            stock_quantity INTEGER,
            unit TEXT,
            sku TEXT,
            barcode TEXT,
            tags TEXT,
            supplier TEXT,
            expiry_date TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        );

        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date TEXT,
            transaction_type TEXT
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            endereco TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            data TEXT,
            horario TEXT,
            valor_total REAL,
            forma_pagamento TEXT,
            valor_recebido REAL,
            troco REAL
        );
    ''')

    # Migrar dados de cada banco de dados
    for table, db_path in db_paths.items():
        old_connection = sqlite3.connect(db_path)
        old_cursor = old_connection.cursor()

        if table_exists(old_cursor, table):
            old_cursor.execute(f"SELECT * FROM {table}")
            data = old_cursor.fetchall()

            # Inserir dados no novo banco de dados
            if table == 'clientes':
                new_cursor.executemany('''
                    INSERT INTO clientes (id, nome, telefone, endereco, email)
                    VALUES (?, ?, ?, ?, ?)
                ''', data)
            elif table == 'pagamentos':
                new_cursor.executemany('''
                    INSERT INTO pagamentos (id, cliente, data, horario, valor_total, forma_pagamento, valor_recebido, troco)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
            elif table == 'produtos':
                new_cursor.executemany('''
                    INSERT INTO Products (product_id, name, code, category, description, sale_price, cost_price, stock_quantity, unit, sku, barcode, tags, supplier, expiry_date, location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
            elif table == 'transactions':
                new_cursor.executemany('''
                    INSERT INTO transactions (transaction_id, description, amount, date, transaction_type)
                    VALUES (?, ?, ?, ?, ?)
                ''', data)
            elif table == 'users':
                new_cursor.executemany('''
                    INSERT INTO users (id, username, password)
                    VALUES (?, ?, ?)
                ''', data)

        old_connection.close()

    new_connection.commit()
    new_connection.close()

if __name__ == "__main__":
    migrate_data()
    print("Migração concluída com sucesso!")