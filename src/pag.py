import os
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QListWidget, QGridLayout, QInputDialog, QMessageBox, QListWidgetItem, QTextEdit, QLineEdit
)
from PySide6.QtCore import Qt

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
    def __init__(self, total_pedido, cliente, produtos, parent=None):
        super().__init__(parent)
        self.total_pedido = total_pedido
        self.cliente = cliente
        self.produtos = produtos
        self.divisoes = []
        self.valor_faltante = total_pedido
        self.pagamentos_realizados = []

        self.setWindowTitle("Conferir e Dividir")
        self.setGeometry(100, 100, 800, 600)

        self.layout_principal = QHBoxLayout(self)
        self.secao_esquerda = QVBoxLayout()
        self.secao_direita = QVBoxLayout()

        self.titulo_esquerda = QLabel("Conferir e Dividir")
        self.secao_esquerda.addWidget(self.titulo_esquerda)

        self.botao_dividir = QPushButton("Dividir valor")
        self.botao_dividir.clicked.connect(self.dividir_pagamento)
        self.secao_esquerda.addWidget(self.botao_dividir)

        self.checkbox_observacoes = QCheckBox("Mostrar Observações")
        self.secao_esquerda.addWidget(self.checkbox_observacoes)

        self.lista_itens = QListWidget()
        for produto in self.produtos:
            item_text = f"{produto['produto']} - Quantidade: {produto['quantidade']}"
            self.lista_itens.addItem(item_text)
        self.secao_esquerda.addWidget(self.lista_itens)

        self.resumo_total = QLabel(f"Total a Pagar: R$ {self.total_pedido:.2f}")
        self.secao_esquerda.addWidget(self.resumo_total)

        self.botao_taxas = QPushButton("Taxas e Descontos (F10)")
        self.botao_imprimir = QPushButton("Imprimir (F6)")
        self.secao_esquerda.addWidget(self.botao_taxas)
        self.secao_esquerda.addWidget(self.botao_imprimir)

        self.titulo_direita = QLabel("Pagamentos")
        self.secao_direita.addWidget(self.titulo_direita)
        self.payment_grid = QGridLayout()

        self.payment_buttons = {
            "Dinheiro": "#4CAF50",
            "Débito": "#2196F3",
            "Crédito": "#FFC107",
            "Pix": "#9E9E9E",
            "V.Refeição": "#FF5722",
            "V. Alimentação": "#FF9800",
            "Fiado": "#F44336"
        }

        row, col = 0, 0
        for text, color in self.payment_buttons.items():
            button = QPushButton(text)
            button.setFixedSize(130, 80)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #ffffff;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 0px;
                    border: 2px solid #333333;
                    padding: 10px;
                }}
            """)
            button.clicked.connect(lambda checked, t=text: self.selecionar_pagamento(t))
            self.payment_grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.secao_direita.addLayout(self.payment_grid)

        self.status_caixa = QLabel(f"Total: R$ {self.total_pedido:.2f}")
        self.secao_direita.addWidget(self.status_caixa)

        self.area_pagamento = QListWidget()
        self.secao_direita.addWidget(self.area_pagamento)

        self.botao_voltar = QPushButton("Voltar")
        self.botao_finalizar = QPushButton("Finalizar (F7)")
        self.botao_finalizar_imprimir = QPushButton("Finalizar e Imprimir (F9)")
        self.botoes_layout = QHBoxLayout()
        self.botoes_layout.addWidget(self.botao_voltar)
        self.botoes_layout.addWidget(self.botao_finalizar)
        self.botoes_layout.addWidget(self.botao_finalizar_imprimir)

        self.secao_direita.addLayout(self.botoes_layout)

        self.layout_principal.addLayout(self.secao_esquerda)
        self.layout_principal.addLayout(self.secao_direita)

    def dividir_pagamento(self):
        partes, ok = QInputDialog.getInt(self, "Dividir em Partes Iguais", "Número de partes:")
        if ok and partes > 0:
            valor_por_parte = self.total_pedido / partes
            self.divisoes = [valor_por_parte] * partes
            QMessageBox.information(self, "Divisão", f"Pagamento dividido em {partes} partes de R$ {valor_por_parte:.2f} cada.")

    def selecionar_pagamento(self, metodo):
        if self.valor_faltante <= 0 and metodo != "Dinheiro":
            QMessageBox.warning(self, "Pagamento Completo", "O valor total já foi pago.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Pagamento com {metodo}")
        dialog.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(dialog)

        # Seção Principal - "Valor"
        layout_valor = QHBoxLayout()

        campo_valor = QLineEdit("0,00")
        campo_valor.setAlignment(Qt.AlignRight)
        campo_valor.setStyleSheet("background-color: #D3D3D3; padding: 10px;")
        layout_valor.addWidget(campo_valor)

        botao_faltante = QPushButton(f"[A] {self.valor_faltante:.2f} (Faltando)")
        botao_faltante.setStyleSheet("background-color: #2196F3; color: white;")
        botao_faltante.clicked.connect(lambda: campo_valor.setText(f"{self.valor_faltante:.2f}"))
        layout_valor.addWidget(botao_faltante)

        botao_limpar = QPushButton("[L] Limpar")
        botao_limpar.setStyleSheet("background-color: #A52A2A; color: white;")
        botao_limpar.clicked.connect(lambda: campo_valor.setText("0,00"))
        layout_valor.addWidget(botao_limpar)

        layout.addLayout(layout_valor)

        # Botões de Valores Rápidos
        layout_rapido = QHBoxLayout()
        for valor in [2, 5, 10, 20, 50, 100]:
            botao_valor = QPushButton(f"{valor:.2f}")
            botao_valor.setStyleSheet("background-color: #4CAF50; color: white;")
            botao_valor.clicked.connect(lambda checked, v=valor: campo_valor.setText(f"{float(campo_valor.text().replace(',', '.')) + v:.2f}"))
            layout_rapido.addWidget(botao_valor)
        layout.addLayout(layout_rapido)

        # Campo de Observação
        campo_observacao = QTextEdit()
        campo_observacao.setPlaceholderText("Observação")
        layout.addWidget(campo_observacao)

        # Rodapé - Botões de Ação
        layout_acoes = QHBoxLayout()

        botao_voltar = QPushButton("Voltar (ESC)")
        botao_voltar.clicked.connect(dialog.close)
        layout_acoes.addWidget(botao_voltar)

        botao_salvar = QPushButton("Salvar (ENTER)")
        botao_salvar.clicked.connect(lambda: self.processar_pagamento(metodo, campo_valor, dialog))
        layout_acoes.addWidget(botao_salvar)

        layout.addLayout(layout_acoes)

        dialog.exec_()

    def processar_pagamento(self, metodo, campo_valor, dialog):
        valor_input = float(campo_valor.text().replace(',', '.'))
        troco = 0

        if metodo == "Dinheiro":
            if valor_input > self.valor_faltante:
                troco = valor_input - self.valor_faltante
                QMessageBox.information(self, "Troco", f"Troco: R$ {troco:.2f}")
        elif valor_input > self.valor_faltante:
            QMessageBox.warning(self, "Erro", "Valor excede o necessário.")
            return

        self.adicionar_valor(metodo, valor_input, troco)
        dialog.close()

    def adicionar_valor(self, metodo, valor, troco=0):
        if valor <= 0:
            return

        self.valor_faltante -= valor
        self.pagamentos_realizados.append({"metodo": metodo, "valor": valor, "troco": troco})
        self.atualizar_interface()

    def atualizar_interface(self):
        self.area_pagamento.clear()
        valor_pago_total = sum([p["valor"] for p in self.pagamentos_realizados])

        for pagamento in self.pagamentos_realizados:
            texto_pagamento = f"{pagamento['metodo']}: R$ {pagamento['valor']:.2f}"
            if pagamento["troco"] > 0:
                texto_pagamento += f" (Troco: R$ {pagamento['troco']:.2f})"
            item = QListWidgetItem(texto_pagamento)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.area_pagamento.addItem(item)

        self.valor_faltante = self.total_pedido - valor_pago_total
        self.status_caixa.setText(f"Total: R$ {self.total_pedido:.2f} | Pago: R$ {valor_pago_total:.2f} | Restante: R$ {self.valor_faltante:.2f}")

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
        if troco and troco > 0:
            QMessageBox.information(self, "Troco", f"Troco: R$ {troco:.2f}")

        if self.valor_faltante <= 0:
            QMessageBox.information(self, "Concluído", "Todos os pagamentos foram concluídos.")
            self.close()