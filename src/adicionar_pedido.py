import os
import sqlite3
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PySide6.QtCore import Signal
from src.produtos import ListaProdutosDialog
from src.pag import PagamentoDialog

# Definição do caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DB_DIR, "clientes.db")

class AdicionarPedidoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adicionar Pedido")
        self.layout = QVBoxLayout(self)
        self.carrinho = []

        # Inicializa a variável de callback
        self.callback = None  

        # Verifica e cria o banco de dados se não existir
        self.verifica_banco_dados()

        # Título
        self.titulo_label = QLabel("Adicionar Pedido")
        self.titulo_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.titulo_label)

        # Informações do Cliente
        self.cliente_layout = QHBoxLayout()

        self.vincular_button = QPushButton("Vincular Cliente", self)
        self.vincular_button.clicked.connect(self.vincular_cliente)
        self.cliente_layout.addWidget(self.vincular_button)

        self.novo_cliente_button = QPushButton("Registrar Novo Cliente", self)
        self.novo_cliente_button.clicked.connect(self.registrar_novo_cliente)
        self.cliente_layout.addWidget(self.novo_cliente_button)

        self.cliente_input = QLineEdit(self)
        self.cliente_input.setPlaceholderText("Nome do Cliente")
        self.telefone_input = QLineEdit(self)
        self.telefone_input.setPlaceholderText("Telefone do Cliente (DDD + Número)")

        self.cliente_layout.addWidget(self.cliente_input)
        self.cliente_layout.addWidget(self.telefone_input)
        self.layout.addLayout(self.cliente_layout)

        # Seção de Inserção de Itens
        self.item_layout = QHBoxLayout()

        # Botão para mostrar produtos
        self.mostrar_produtos_button = QPushButton("Mostrar Produtos", self)
        self.mostrar_produtos_button.clicked.connect(self.mostrar_produtos)
        self.item_layout.addWidget(self.mostrar_produtos_button)

        self.layout.addLayout(self.item_layout)

        # Tabela de Itens Adicionados
        self.tabela_pedido = QTableWidget(self)
        self.tabela_pedido.setColumnCount(5)
        self.tabela_pedido.setHorizontalHeaderLabels(["Produto", "Quantidade", "Subtotal", "Ação"])
        self.layout.addWidget(self.tabela_pedido)

        # Total Geral
        self.total_label = QLabel("Total do Pedido: R$ 0.00", self)
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.total_label)

        # Botões de Ação
        self.botoes_layout = QHBoxLayout()
        self.finalizar_button = QPushButton("Finalizar Pedido", self)
        self.finalizar_button.clicked.connect(self.finalizar_pedido)
        self.cancelar_button = QPushButton("Cancelar", self)
        self.cancelar_button.clicked.connect(self.cancelar_pedido)
        self.limpar_button = QPushButton("Limpar Pedido", self)
        self.limpar_button.clicked.connect(self.limpar_pedido)

        self.botoes_layout.addWidget(self.finalizar_button)
        self.botoes_layout.addWidget(self.cancelar_button)
        self.botoes_layout.addWidget(self.limpar_button)

        self.layout.addLayout(self.botoes_layout)

        self.itens = []  # Para armazenar os itens do pedido

    def set_callback(self, callback):
        """Define uma função de callback que pode ser chamada posteriormente."""
        self.callback = callback

    def vincular_cliente(self):
        # Abre a janela de vinculação de cliente
        dialog = VincularClienteDialog(self)
        dialog.cliente_selecionado.connect(self.preencher_cliente)  # Conecta o sinal
        dialog.exec()

    def registrar_novo_cliente(self):
        """Abre um diálogo para registrar um novo cliente."""
        dialog = RegistrarClienteDialog(self)
        dialog.cliente_registrado.connect(self.preencher_cliente)  # Conecta o sinal
        dialog.exec()

    def preencher_cliente(self, nome, telefone):
        """Preenche os campos de cliente com os dados do cliente selecionado."""
        self.cliente_input.setText(nome)
        self.telefone_input.setText(telefone)

    def verifica_banco_dados(self):
        # Verifica se o diretório existe, se não, cria
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)

        # Verifica se o banco de dados existe, se não, cria
        if not os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(''' 
                CREATE TABLE clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    endereco TEXT,
                    email TEXT
                )
            ''')
            conn.commit()
            conn.close()

    def mostrar_produtos(self):
        """Abre um diálogo para mostrar todos os produtos disponíveis."""
        dialog = ListaProdutosDialog(self)
        dialog.produto_selecionado.connect(self.adicionar_item)  # Conecta o sinal de produto selecionado
        dialog.exec()

    def adicionar_item(self, produto):
        """Adiciona o produto selecionado à tabela de pedido."""
        nome = produto['name']
        quantidade = produto['quantity']  # Agora pegamos a quantidade diretamente do dict produto
        subtotal = produto['price'] * quantidade

        # Adiciona à tabela
        row_position = self.tabela_pedido.rowCount()
        self.tabela_pedido.insertRow(row_position)
        self.tabela_pedido.setItem(row_position, 0, QTableWidgetItem(nome))
        self.tabela_pedido.setItem(row_position, 1, QTableWidgetItem(str(quantidade)))
        self.tabela_pedido.setItem(row_position, 2, QTableWidgetItem(f"R$ {subtotal:.2f}"))

        # Adiciona um botão de remover
        remove_button = QPushButton("Remover")
        remove_button.clicked.connect(lambda: self.remover_item(row_position))
        self.tabela_pedido.setCellWidget(row_position, 3, remove_button)

        # Atualiza total
        self.atualizar_total()

    def remover_item(self, row):
        """Remove o item da tabela de pedido."""
        self.tabela_pedido.removeRow(row)
        self.atualizar_total()

    def atualizar_total(self):
        """Atualiza o total do pedido."""
        total = 0.0
        for row in range(self.tabela_pedido.rowCount()):
            subtotal = self.tabela_pedido.item(row, 2)
            if subtotal:
                total += float(subtotal.text().replace("R$ ", "").replace(",", "."))
        self.total_label.setText(f"Total do Pedido: R$ {total:.2f}")

    def finalizar_pedido(self):
        """Abre a janela de forma de pagamento."""
        total = float(self.total_label.text().replace("Total do Pedido: R$ ", "").replace(",", "."))
        dialog = PagamentoDialog(total, self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Pedido Finalizado", "Seu pedido foi finalizado com sucesso.")
            self.limpar_campos()
            self.tabela_pedido.clearContents()
            self.tabela_pedido.setRowCount(0)
            self.itens.clear()
            self.atualizar_total()
    def cancelar_pedido(self):
        self.limpar_campos()
        self.tabela_pedido.clearContents()
        self.tabela_pedido.setRowCount(0)
        self.itens.clear()
        self.atualizar_total()

    def limpar_pedido(self):
        self.tabela_pedido.clearContents()
        self.tabela_pedido.setRowCount(0)
        self.itens.clear()
        self.atualizar_total()

    def limpar_campos(self):
        self.cliente_input.clear()
        self.telefone_input.clear()


class VincularClienteDialog(QDialog):
    cliente_selecionado = Signal(str, str)  # Sinal para enviar nome e telefone

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Vincular Cliente")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        self.clientes_table = QTableWidget(self)
        self.clientes_table.setColumnCount(4)
        self.clientes_table.setHorizontalHeaderLabels(["Nome", "Telefone", "Endereço", "E-mail"])
        self.layout.addWidget(self.clientes_table)

        self.carregar_clientes()

        self.clientes_table.cellDoubleClicked.connect(self.selecionar_cliente)  # Conecta o evento de clique duplo

    def carregar_clientes(self):
        """Carrega clientes do banco de dados."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT nome, telefone, endereco, email FROM clientes")
            clientes = cursor.fetchall()
            conn.close()

            self.clientes_table.setRowCount(len(clientes))

            for row_index, cliente in enumerate(clientes):
                for column_index, dado in enumerate(cliente):
                    self.clientes_table.setItem(row_index, column_index, QTableWidgetItem(dado))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar clientes: {e}")

    def selecionar_cliente(self, row, column):
        """Seleciona um cliente e emite um sinal com o nome e telefone."""
        nome = self.clientes_table.item(row, 0).text()
        telefone = self.clientes_table.item(row, 1).text()
        self.cliente_selecionado.emit(nome, telefone)  # Emite o sinal com os dados do cliente
        self.close()  # Fecha o diálogo após selecionar


class RegistrarClienteDialog(QDialog):
    cliente_registrado = Signal(str, str)  # Sinal para enviar nome e telefone

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Registrar Novo Cliente")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)

        # Campos para entrada de dados do cliente
        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Nome")
        self.telefone_input = QLineEdit(self)
        self.telefone_input.setPlaceholderText("Telefone (DDD + Número)")
        self.endereco_input = QLineEdit(self)
        self.endereco_input.setPlaceholderText("Endereço (opcional)")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("E-mail (opcional)")

        self.layout.addWidget(self.nome_input)
        self.layout.addWidget(self.telefone_input)
        self.layout.addWidget(self.endereco_input)
        self.layout.addWidget(self.email_input)

        self.registrar_button = QPushButton("Registrar", self)
        self.registrar_button.clicked.connect(self.registrar_cliente)
        self.layout.addWidget(self.registrar_button)

    def registrar_cliente(self):
        """Registra um novo cliente no banco de dados."""
        nome = self.nome_input.text()
        telefone = self.telefone_input.text()
        endereco = self.endereco_input.text()
        email = self.email_input.text()

        if not nome or not telefone:
            QMessageBox.warning(self, "Erro", "Nome e telefone são obrigatórios.")
            return

        try:
            # Adiciona o cliente ao banco de dados
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (nome, telefone, endereco, email) VALUES (?, ?, ?, ?)",
                           (nome, telefone, endereco, email))
            conn.commit()
            conn.close()

            # Emite o sinal com os dados do cliente registrado
            self.cliente_registrado.emit(nome, telefone)
            QMessageBox.information(self, "Sucesso", "Cliente registrado com sucesso!")
            self.close()  # Fecha o diálogo após registrar
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao registrar cliente: {e}")


# Se você precisar executar o aplicativo, você pode adicionar um método main aqui
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_widget = AdicionarPedidoWidget()
    main_widget.show()
    sys.exit(app.exec())