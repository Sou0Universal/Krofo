import os
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QGridLayout, QCheckBox, QListWidget
)

# Configuração do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DB_DIR, "pagamentos.db")

os.makedirs(DB_DIR, exist_ok=True)

def criar_banco_se_nao_existir():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            data TEXT,
            horario TEXT,
            valor_total REAL,
            forma_pagamento TEXT,
            valor_recebido REAL,
            troco REAL
        )
    """)
    conn.commit()
    conn.close()

criar_banco_se_nao_existir()

class PagamentoDialog(QDialog):
    def __init__(self, total_pedido, cliente, parent=None):
        super().__init__(parent)
        self.total_pedido = total_pedido
        self.cliente = cliente
        self.setWindowTitle("Conferir e Dividir")
        self.setGeometry(100, 100, 800, 600)

        self.layout_principal = QHBoxLayout(self)
        self.secao_esquerda = QVBoxLayout()
        self.secao_direita = QVBoxLayout()

        # Seção Esquerda
        self.titulo_esquerda = QLabel("Conferir e Dividir")
        self.secao_esquerda.addWidget(self.titulo_esquerda)

        self.botao_dividir = QPushButton("Selecionar para Dividir")
        self.secao_esquerda.addWidget(self.botao_dividir)

        self.checkbox_observacoes = QCheckBox("Mostrar Observações")
        self.secao_esquerda.addWidget(self.checkbox_observacoes)

        self.lista_itens = QListWidget()
        self.lista_itens.addItem("Alabama Clássico (promo) - R$ 13,50")
        self.secao_esquerda.addWidget(self.lista_itens)

        self.resumo_total = QLabel("1 Pessoa, Total a Pagar: R$ 13,50")
        self.secao_esquerda.addWidget(self.resumo_total)

        self.botao_taxas = QPushButton("Taxas e Descontos (F10)")
        self.botao_imprimir = QPushButton("Imprimir (F6)")
        self.secao_esquerda.addWidget(self.botao_taxas)
        self.secao_esquerda.addWidget(self.botao_imprimir)

        # Seção Direita
        self.titulo_direita = QLabel("Pagamentos")
        self.secao_direita.addWidget(self.titulo_direita)

        self.payment_grid = QGridLayout()
        self.payment_buttons = {
            "Dinheiro": "green",
            "Débito": "blue",
            "Crédito": "blue",
            "Pix": "gray",
            "Vale Refeição": "orange",
            "Vale Alimentação": "yellow",
            "Fiado": "red",
            "Outros": "purple"
        }

        row, col = 0, 0
        for text, color in self.payment_buttons.items():
            button = QPushButton(text)
            button.setStyleSheet(f"background-color: {color}; color: white;")
            button.clicked.connect(lambda checked, t=text: self.selecionar_pagamento(t))
            self.payment_grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.secao_direita.addLayout(self.payment_grid)

        self.status_caixa = QLabel("Caixa aberto")
        self.secao_direita.addWidget(self.status_caixa)

        self.area_pagamento = QLabel("Nenhum Pagamento Adicionado")
        self.secao_direita.addWidget(self.area_pagamento)

        # Barra Inferior
        self.botao_voltar = QPushButton("Voltar")
        self.botao_finalizar = QPushButton("Finalizar (F7)")
        self.botao_finalizar_imprimir = QPushButton("Finalizar e Imprimir (F9)")
        self.layout_inferior = QHBoxLayout()
        self.layout_inferior.addWidget(self.botao_voltar)
        self.layout_inferior.addWidget(self.botao_finalizar)
        self.layout_inferior.addWidget(self.botao_finalizar_imprimir)

        # Adicionar seções ao layout principal
        self.layout_principal.addLayout(self.secao_esquerda)
        self.layout_principal.addLayout(self.secao_direita)
        self.layout_principal.addLayout(self.layout_inferior)

    def selecionar_pagamento(self, metodo):
        if metodo == "Dinheiro":
            self.pagar_em_dinheiro()
        else:
            self.registrar_pagamento(metodo)

    def pagar_em_dinheiro(self):
        valor, ok = QInputDialog.getDouble(self, "Pagamento em Dinheiro", "Valor recebido:")
        if ok:
            troco = valor - self.total_pedido
            if troco < 0:
                QMessageBox.warning(self, "Erro", "Valor recebido insuficiente.")
                return
            self.registrar_pagamento("Dinheiro", valor, troco)

    def registrar_pagamento(self, metodo, valor_recebido=None, troco=None):
        if valor_recebido is None:
            valor_recebido = self.total_pedido
            troco = 0

        data_atual = datetime.now().strftime("%Y-%m-%d")
        horario_atual = datetime.now().strftime("%H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pagamentos (cliente, data, horario, valor_total, forma_pagamento, valor_recebido, troco)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.cliente, data_atual, horario_atual, self.total_pedido, metodo, valor_recebido, troco))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Pagamento", "Pagamento confirmado com sucesso!")
        if troco > 0:
            QMessageBox.information(self, "Troco", f"Troco: R$ {troco:.2f}")

if __name__ == "__main__":
    app = QApplication([])
    dialog = PagamentoDialog(13.50, "Cliente Exemplo")
    dialog.exec()