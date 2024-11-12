from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
import sqlite3
import os
from PySide6.QtCore import QDateTime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DB_DIR, "transactions.db")

class AbrirCaixaWidget(QWidget):
    def __init__(self, fechar_caixa_callback):
        super().__init__()

        self.fechar_caixa_callback = fechar_caixa_callback
        self.setWindowTitle("Abertura de Caixa")
        self.setGeometry(300, 300, 400, 200)

        main_layout = QVBoxLayout(self)

        valor_label = QLabel("Valor Inicial:")
        self.valor_inicial_input = QLineEdit()
        self.valor_inicial_input.setPlaceholderText("Digite o valor inicial")

        valor_layout = QHBoxLayout()
        valor_layout.addWidget(valor_label)
        valor_layout.addWidget(self.valor_inicial_input)

        abrir_button = QPushButton("Abrir Caixa")
        abrir_button.clicked.connect(self.abrir_caixa)
        abrir_button.setObjectName("abrirCaixaButton")

        main_layout.addLayout(valor_layout)
        main_layout.addWidget(abrir_button)

    def get_state(self):
        return {
            'valor_inicial': self.valor_inicial_input.text()
        }

    def set_state(self, state):
        self.valor_inicial_input.setText(state.get('valor_inicial', ''))

    def abrir_caixa(self):
        try:
            valor_inicial = float(self.valor_inicial_input.text().replace('R$', '').replace(',', '.').strip())
            if valor_inicial <= 0:
                raise ValueError

            self.salvar_valor_inicial_no_bd(valor_inicial)
            self.fechar_caixa_callback(valor_inicial, "Abertura de Caixa")
            QMessageBox.information(self, "Sucesso", "Caixa aberto com sucesso!")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira um valor inicial válido.")

    def salvar_valor_inicial_no_bd(self, valor_inicial):
        date_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO close_registers (date, opening_value)
            VALUES (?, ?)
        ''', (date_time, valor_inicial))

        connection.commit()
        connection.close()