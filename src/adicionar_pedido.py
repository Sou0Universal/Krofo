import os
import sqlite3
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QDialog
)
from PySide6.QtCore import Signal

# Definição do caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DB_DIR, "clientes.db")
PRODUTOS_DB_PATH = os.path.join(BASE_DIR, "..", "data", "produtos.db")  # Ajuste o caminho conforme necessário

class AdicionarPedidoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adicionar Pedido")
        self.layout = QVBoxLayout(self)

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

        self.cliente_input = QLineEdit(self)
        self.cliente_input.setPlaceholderText("Nome do Cliente")
        self.telefone_input = QLineEdit(self)
        self.telefone_input.setPlaceholderText("Telefone do Cliente (DDD + Número)")

        self.cliente_layout.addWidget(self.cliente_input)
        self.cliente_layout.addWidget(self.telefone_input)
        self.layout.addLayout(self.cliente_layout)

        # Seção de Inserção de Itens
        self.item_layout = QHBoxLayout()
        
        self.produto_input = QComboBox(self)
        self.produto_input.currentIndexChanged.connect(self.atualizar_preco_unitario)  # Atualiza preço ao mudar produto
        self.carregar_produtos()  # Carregar produtos do banco de dados
        self.quantidade_input = QSpinBox(self)
        self.quantidade_input.setMaximum(1000)

        # Inicialização correta do campo de preço unitário
        self.preco_unitario_input = QLineEdit(self)
        self.preco_unitario_input.setPlaceholderText("Preço Unitário")
        self.preco_unitario_input.setReadOnly(True)  # O campo é somente leitura

        self.desconto_input = QLineEdit(self)
        self.desconto_input.setPlaceholderText("Desconto (opcional)")

        self.item_layout.addWidget(self.produto_input)
        self.item_layout.addWidget(self.quantidade_input)
        self.item_layout.addWidget(self.preco_unitario_input)
        self.item_layout.addWidget(self.desconto_input)

        self.adicionar_button = QPushButton("Adicionar ao Pedido", self)
        self.adicionar_button.clicked.connect(self.adicionar_item)
        self.item_layout.addWidget(self.adicionar_button)

        self.layout.addLayout(self.item_layout)

        # Tabela de Itens Adicionados
        self.tabela_pedido = QTableWidget(self)
        self.tabela_pedido.setColumnCount(5)
        self.tabela_pedido.setHorizontalHeaderLabels(["Produto", "Quantidade", "Preço Unitário", "Subtotal", "Ação"])
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
        dialog.exec_()

    def preencher_cliente(self, nome, telefone):
        """Preenche os campos de cliente com os dados do cliente selecionado."""
        self.cliente_input.setText(nome)
        self.telefone_input.setText(telefone)

    def carregar_produtos(self):
        """Carrega produtos do banco de dados 'produtos.db'."""
        self.produto_input.clear()  # Limpa a lista de produtos existente

        print("Tentando conectar ao banco de dados em:", PRODUTOS_DB_PATH)  # Para depuração

        try:
            conn = sqlite3.connect(PRODUTOS_DB_PATH)  # Conecte-se ao banco de produtos
            cursor = conn.cursor()
            cursor.execute("SELECT product_id, name, sale_price, stock_quantity FROM Products")
            produtos = cursor.fetchall()
            for product_id, name, sale_price, stock_quantity in produtos:
                # Adiciona o nome do produto ao ComboBox, incluindo preço e estoque
                self.produto_input.addItem(f"{name} - Preço: R$ {sale_price:.2f} - Estoque: {stock_quantity}", product_id)
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao banco de dados: {e}")

    def atualizar_preco_unitario(self):
        """Atualiza o campo de preço unitário com o preço do produto selecionado."""
        current_index = self.produto_input.currentIndex()
        if current_index >= 0:
            price_text = self.produto_input.currentText().split(" - Preço: R$ ")[1]
            self.preco_unitario_input.setText(price_text.split(" - Estoque: ")[0])  # Pega apenas o preço

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

    def adicionar_item(self):
        # Obter dados dos campos
        produto = self.produto_input.currentText()
        quantidade = self.quantidade_input.value()

        # Validação do preço unitário
        try:
            preco_unitario = float(self.preco_unitario_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço Unitário deve ser um número válido.")
            return
        
        desconto = float(self.desconto_input.text() or 0)

        # Calcular subtotal
        subtotal = (preco_unitario * quantidade) - desconto

        # Adicionar à tabela
        row_position = self.tabela_pedido.rowCount()
        self.tabela_pedido.insertRow(row_position)
        self.tabela_pedido.setItem(row_position, 0, QTableWidgetItem(produto))
        self.tabela_pedido.setItem(row_position, 1, QTableWidgetItem(str(quantidade)))
        self.tabela_pedido.setItem(row_position, 2, QTableWidgetItem(f"R$ {preco_unitario:.2f}"))
        self.tabela_pedido.setItem(row_position, 3, QTableWidgetItem(f"R$ {subtotal:.2f}"))

        # Adicionar botão para remover item
        remove_button = QPushButton("Remover")
        remove_button.clicked.connect(lambda: self.remover_item(row_position))
        self.tabela_pedido.setCellWidget(row_position, 4, remove_button)

        # Atualizar total
        self.itens.append((produto, quantidade, preco_unitario, subtotal))
        self.atualizar_total()

        # Limpar campos após adicionar
        self.limpar_campos()

    def remover_item(self, row):
        self.tabela_pedido.removeRow(row)
        del self.itens[row]  # Remover item da lista
        self.atualizar_total()

    def atualizar_total(self):
        total = sum(item[3] for item in self.itens)  # Somar subtotais
        self.total_label.setText(f"Total do Pedido: R$ {total:.2f}")

    def finalizar_pedido(self):
        # Aqui você pode implementar a lógica para salvar o pedido no banco de dados
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
        self.produto_input.setCurrentIndex(0)
        self.quantidade_input.setValue(1)
        self.preco_unitario_input.clear()
        self.desconto_input.clear()


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
        # Carrega clientes do banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, telefone, endereco, email FROM clientes")
        clientes = cursor.fetchall()
        conn.close()

        self.clientes_table.setRowCount(len(clientes))

        for row_index, cliente in enumerate(clientes):
            for column_index, dado in enumerate(cliente):
                self.clientes_table.setItem(row_index, column_index, QTableWidgetItem(dado))

    def selecionar_cliente(self, row, column):
        """Seleciona um cliente e emite um sinal com o nome e telefone."""
        nome = self.clientes_table.item(row, 0).text()
        telefone = self.clientes_table.item(row, 1).text()
        self.cliente_selecionado.emit(nome, telefone)  # Emite o sinal com os dados do cliente
        self.close()  # Fecha o diálogo após selecionar


# Se você precisar executar o aplicativo, você pode adicionar um método main aqui
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_widget = AdicionarPedidoWidget()
    main_widget.show()
    sys.exit(app.exec())