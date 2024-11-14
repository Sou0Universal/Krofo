from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox
import sqlite3
import os
from PySide6.QtCore import QDateTime
from .Entrada_Saida import EntradaSaidaWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DB_DIR, "sistema.db")

class FecharCaixaWidget(QWidget):
    def __init__(self, dashboard, fechar_caixa_callback):
        super().__init__()
        self.dashboard = dashboard
        
        self.create_database()
        
        self.setWindowTitle("Fechar Caixa")
        self.setGeometry(150, 150, 600, 400)

        main_layout = QVBoxLayout(self)

        buttons_layout = QHBoxLayout()

        entrada_saida_button = QPushButton("Entradas e Saídas")
        entrada_saida_button.setObjectName("entradaSaidaButton")
        entrada_saida_button.clicked.connect(self.open_entrada_saida)

        fechar_button = QPushButton("Fechar Caixa")
        fechar_button.setObjectName("fecharCaixaButton")
        fechar_button.clicked.connect(lambda: self.fechar_caixa(fechar_caixa_callback))
        
        buttons_layout.addWidget(entrada_saida_button)
        buttons_layout.addWidget(fechar_button)

        main_layout.addLayout(buttons_layout)

        self.observacao_input = QLineEdit()
        self.observacao_input.setPlaceholderText("Observação")
        main_layout.addWidget(self.observacao_input)

        right_layout = QVBoxLayout()

        self.saldo_inicial_label = QLabel("Saldo Inicial: R$0,00")
        self.total_entradas_label = QLabel("Entradas: R$0,00")
        self.total_saidas_label = QLabel("Saídas: R$0,00")
        self.saldo_final_label = QLabel("Saldo Final: R$0,00")

        right_layout.addWidget(self.saldo_inicial_label)
        right_layout.addWidget(self.total_entradas_label)
        right_layout.addWidget(self.total_saidas_label)
        right_layout.addWidget(self.saldo_final_label)

        self.historico_text = QTextEdit()
        self.historico_text.setReadOnly(True)
        right_layout.addWidget(self.historico_text)

        main_layout.addLayout(right_layout)

        self.carregar_saldos()

    def get_state(self):
        return {
            'observacao': self.observacao_input.text(),
            'historico': self.historico_text.toHtml()
        }

    def set_state(self, state):
        self.observacao_input.setText(state.get('observacao', ''))
        self.historico_text.setHtml(state.get('historico', ''))

    def open_entrada_saida(self):
        tab_name = "Entradas e Saídas"
        existing_tabs = [self.dashboard.tab_widget.tabText(i) for i in range(self.dashboard.tab_widget.count())]

        if tab_name not in existing_tabs:
            entrada_saida_tab = QWidget()
            layout = QVBoxLayout()
            entrada_saida_widget = EntradaSaidaWindow(close_callback=self.atualizar_historico)
            layout.addWidget(entrada_saida_widget)
            entrada_saida_tab.setLayout(layout)
            index = self.dashboard.tab_widget.addTab(entrada_saida_tab, tab_name)
        else:
            index = existing_tabs.index(tab_name)
        
        self.dashboard.tab_widget.setCurrentIndex(index)

    def close_tab_by_name(self, tab_name):
        for i in range(self.dashboard.tab_widget.count()):
            if self.dashboard.tab_widget.tabText(i) == tab_name:
                self.dashboard.tab_widget.removeTab(i)
                break

    def carregar_saldos(self):
        saldo_inicial = self.obter_saldo_inicial()
        self.atualizar_resumo(saldo_inicial)

    def obter_saldo_inicial(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT opening_value FROM close_registers ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0.0

    def atualizar_resumo(self, saldo_inicial):
        total_entradas, total_saidas = self.calcular_totais()

        self.saldo_inicial_label.setText(f"Saldo Inicial: R${saldo_inicial:.2f}")
        self.total_entradas_label.setText(f"Entradas: R${total_entradas:.2f}")
        self.total_saidas_label.setText(f"Saídas: R${total_saidas:.2f}")
        saldo_final = saldo_inicial + total_entradas - total_saidas
        self.saldo_final_label.setText(f"Saldo Final: R${saldo_final:.2f}")

    def calcular_totais(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'entrada'")
        total_entradas = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'saida'")
        total_saidas = cursor.fetchone()[0] or 0.0

        connection.close()
        
        return total_entradas, total_saidas

    def fechar_caixa(self, callback):
        saldo_inicial = self.obter_saldo_inicial()
        total_entradas, total_saidas = self.calcular_totais()
        saldo_final = saldo_inicial + total_entradas - total_saidas

        self.salvar_historico_no_bd(saldo_inicial, saldo_final, total_entradas, total_saidas)

        # Limpar a tabela de transações
        self.limpar_transacoes()

        # Atualizar os rótulos
        self.saldo_inicial_label.setText("Saldo Inicial: R$0,00")
        self.total_entradas_label.setText("Entradas: R$0,00")
        self.total_saidas_label.setText("Saídas: R$0,00")
        self.saldo_final_label.setText("Saldo Final: R$0,00")

        self.historico_text.clear()

        observacao = self.observacao_input.text()
        callback(saldo_final, observacao)

    def limpar_transacoes(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM transactions')
        connection.commit()
        connection.close()

    def salvar_historico_no_bd(self, saldo_inicial, saldo_final, total_entradas, total_saidas):
        date_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        observacao = self.observacao_input.text()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO close_registers (date, opening_value, closing_value, total_entries, total_exits, observations)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date_time, saldo_inicial, saldo_final, total_entradas, total_saidas, observacao))

        connection.commit()
        connection.close()

    def adicionar_no_historico(self, amount, descricao, observacao=""):
        date_time = QDateTime.currentDateTime().toString("hh:mm")
        historico_entry = f"""
        <div style='border-bottom: 1px solid #ccc; padding: 5px;'>
            <b>{date_time}</b> - <b>R${amount:.2f}</b> - {descricao}
            {f"- {observacao}" if observacao else ""}
        </div>
        """
        self.historico_text.append(historico_entry)

    def atualizar_historico(self):
        self.historico_text.clear()
        saldo_inicial = self.obter_saldo_inicial()
        self.adicionar_no_historico(saldo_inicial, "Abertura do caixa")

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        # Separar e exibir entradas
        cursor.execute("SELECT date, amount, note FROM transactions WHERE type = 'entrada' ORDER BY date")
        entradas = cursor.fetchall()
        if entradas:
            self.historico_text.append("<b>Entradas:</b>")
            for date, amount, note in entradas:
                self.adicionar_no_historico(amount, "Entrada", note)

        # Separar e exibir saídas
        cursor.execute("SELECT date, amount, note FROM transactions WHERE type = 'saida' ORDER BY date")
        saidas = cursor.fetchall()
        if saidas:
            self.historico_text.append("<b>Saídas:</b>")
            for date, amount, note in saidas:
                self.adicionar_no_historico(amount, "Saída", note)

        connection.close()

        # Atualizar o resumo
        total_entradas, total_saidas = self.calcular_totais()
        self.atualizar_resumo(saldo_inicial)

    def create_database(self):
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
                date TEXT,
                type TEXT,
                amount REAL,
                note TEXT
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