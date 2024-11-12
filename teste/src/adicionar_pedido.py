from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QMessageBox
)
from datetime import datetime
import sqlite3
import os

class AdicionarPedidoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.callback = None
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

    def set_callback(self, callback):
        self.callback = callback

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
        connection = sqlite3.connect(db_path, timeout=10)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT sale_price FROM Products WHERE product_id = ?", (product_id,))
            result = cursor.fetchone()
            if result:
                sale_price = result[0]
                total_value = sale_price * quantity

                cursor.execute('''
                    INSERT INTO Orders (product_id, quantity, order_date)
                    VALUES (?, ?, ?)
                ''', (product_id, quantity, order_date))
                connection.commit()

                trans_connection = sqlite3.connect(os.path.join(os.getcwd(), "data", "transactions.db"), timeout=10)
                trans_cursor = trans_connection.cursor()
                try:
                    trans_cursor.execute('''
                        INSERT INTO transactions (type, amount, note, date) 
                        VALUES (?, ?, ?, ?)
                    ''', ("entrada", total_value, f"Venda produto {self.product_input.currentText()}", order_date))
                    trans_connection.commit()
                finally:
                    trans_connection.close()

                if self.callback:
                    self.callback("entrada", total_value)

                QMessageBox.information(self, "Sucesso", "Pedido adicionado com sucesso!")
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Produto não encontrado.")
        finally:
            connection.close()