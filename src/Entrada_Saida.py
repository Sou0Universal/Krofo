import os
import sqlite3
from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime

DB_PATH = os.path.join(os.getcwd(), "data", "sistema.db")

class EntradaSaidaWindow(QtWidgets.QWidget):
    def __init__(self, close_callback=None):
        super().__init__()
        self.setWindowTitle("Adicionar Entrada/Saída")
        self.setGeometry(150, 150, 400, 200)
        self.close_callback = close_callback

        layout = QtWidgets.QVBoxLayout(self)

        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["entrada", "saida"])
        layout.addWidget(self.type_combo)

        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setPlaceholderText("Valor")
        layout.addWidget(self.amount_input)

        self.note_input = QtWidgets.QLineEdit()
        self.note_input.setPlaceholderText("Observação")
        layout.addWidget(self.note_input)

        add_button = QtWidgets.QPushButton("Adicionar")
        add_button.clicked.connect(self.add_entry)
        layout.addWidget(add_button)

    def add_entry(self):
        entry_type = self.type_combo.currentText()
        amount = self.amount_input.text()
        note = self.note_input.text()

        if not amount:
            return

        try:
            amount = float(amount.replace('R$', '').replace(',', '.').strip())
        except ValueError:
            return

        self.save_transaction(entry_type, amount, note)
        
        if self.close_callback:
            self.close_callback()

    def save_transaction(self, trans_type, amount, note):
        date_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO transactions (type, amount, note, date) VALUES (?, ?, ?, ?)
        ''', (trans_type, amount, note, date_time))
        connection.commit()
        connection.close()