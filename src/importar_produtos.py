import os
import sqlite3
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QComboBox, QTextEdit, QFormLayout, QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox
)
from datetime import datetime

class ImportarProdutosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar Novo Produto")
        self.setGeometry(300, 300, 500, 600)
        layout = QFormLayout(self)
        self.name_input = QLineEdit()
        layout.addRow("Nome do Produto:", self.name_input)
        self.code_input = QLineEdit()
        layout.addRow("Código do Produto:", self.code_input)
        self.category_input = QComboBox()
        self.category_input.addItems(["Alimentos", "Bebidas", "Limpeza"])
        layout.addRow("Categoria:", self.category_input)
        self.description_input = QTextEdit()
        layout.addRow("Descrição:", self.description_input)
        self.sale_price_input = QDoubleSpinBox()
        self.sale_price_input.setMaximum(10000)
        layout.addRow("Preço de Venda:", self.sale_price_input)
        self.cost_price_input = QDoubleSpinBox()
        self.cost_price_input.setMaximum(10000)
        layout.addRow("Preço de Custo:", self.cost_price_input)
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(1000)
        layout.addRow("Quantidade em Estoque:", self.stock_input)
        self.unit_input = QComboBox()
        self.unit_input.addItems(["Unidade", "Kg", "Litro"])
        layout.addRow("Unidade de Medida:", self.unit_input)
        self.image_button = QPushButton("Selecionar Imagem")
        self.image_button.clicked.connect(self.select_image)
        layout.addRow("Imagens do Produto:", self.image_button)
        self.sku_input = QLineEdit()
        layout.addRow("SKU:", self.sku_input)
        self.barcode_input = QLineEdit()
        layout.addRow("Código de Barras:", self.barcode_input)
        self.tags_input = QLineEdit()
        layout.addRow("Tags:", self.tags_input)
        self.supplier_input = QLineEdit()
        layout.addRow("Fornecedor:", self.supplier_input)
        self.expiry_date_input = QLineEdit()
        layout.addRow("Data de Validade:", self.expiry_date_input)
        self.location_input = QLineEdit()
        layout.addRow("Localização no Estoque:", self.location_input)
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_product)
        layout.addRow(self.save_button)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.close)
        layout.addRow(self.cancel_button)
        self.clear_button = QPushButton("Limpar Campos")
        self.clear_button.clicked.connect(self.clear_fields)
        layout.addRow(self.clear_button)
        self.init_db()

    def init_db(self):
        os.makedirs('data', exist_ok=True)
        db_path = os.path.join('data', 'produtos.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
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
            )
        ''')
        connection.commit()
        connection.close()

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar Imagem", "", "Images (*.png *.xpm *.jpg)")
        if file_path:
            QMessageBox.information(self, "Imagem Selecionada", f"Imagem '{file_path}' selecionada.")

    def save_product(self):
        name = self.name_input.text()
        code = self.code_input.text()
        category = self.category_input.currentText()
        description = self.description_input.toPlainText()
        sale_price = self.sale_price_input.value()
        cost_price = self.cost_price_input.value()
        stock = self.stock_input.value()
        unit = self.unit_input.currentText()
        sku = self.sku_input.text()
        barcode = self.barcode_input.text()
        tags = self.tags_input.text()
        supplier = self.supplier_input.text()
        expiry_date = self.expiry_date_input.text()
        location = self.location_input.text()
        if not name:
            QMessageBox.warning(self, "Erro", "O nome do produto é obrigatório.")
            return
        db_path = os.path.join('data', 'produtos.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Products (name, code, category, description, sale_price, cost_price, stock_quantity, unit, sku, barcode, tags, supplier, expiry_date, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, code, category, description, sale_price, cost_price, stock, unit, sku, barcode, tags, supplier, expiry_date, location))
        connection.commit()
        connection.close()
        QMessageBox.information(self, "Sucesso", "Produto salvo com sucesso!")
        self.clear_fields()

    def clear_fields(self):
        self.name_input.clear()
        self.code_input.clear()
        self.description_input.clear()
        self.sale_price_input.setValue(0)
        self.cost_price_input.setValue(0)
        self.stock_input.setValue(0)
        self.sku_input.clear()
        self.barcode_input.clear()
        self.tags_input.clear()
        self.supplier_input.clear()
        self.expiry_date_input.clear()
        self.location_input.clear()

class AdicionarPedidoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar Pedido")
        self.setGeometry(300, 300, 400, 300)
        layout = QVBoxLayout(self)
        self.product_input = QComboBox()
        self.load_products()
        layout.addWidget(QLabel("Produto:"))
        layout.addWidget(self.product_input)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1000)
        layout.addWidget(QLabel("Quantidade:"))
        layout.addWidget(self.quantity_input)
        self.add_button = QPushButton("Adicionar Pedido")
        self.add_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_button)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

    def load_products(self):
        db_path = os.path.join('data', 'produtos.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT product_id, name FROM Products")
        products = cursor.fetchall()
        connection.close()
        for product_id, name in products:
            self.product_input.addItem(name, product_id)

    def add_order(self):
        product_id = self.product_input.currentData()
        quantity = self.quantity_input.value()
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db_path = os.path.join('data', 'produtos.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO Orders (product_id, quantity, order_date)
            VALUES (?, ?, ?)
        ''', (product_id, quantity, order_date))
        connection.commit()
        connection.close()
        QMessageBox.information(self, "Sucesso", "Pedido adicionado com sucesso!")
        self.close()

def init_db():
    os.makedirs('data', exist_ok=True)
    db_path = os.path.join('data', 'produtos.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
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
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY(product_id) REFERENCES Products(product_id)
        )
    ''')
    connection.commit()
    connection.close()

init_db()