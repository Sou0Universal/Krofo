import os
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QPushButton, QHeaderView, QLabel, QHBoxLayout, QFrame, QSpinBox, QGridLayout
)
from PySide6.QtCore import Signal

# Definição do caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "data")
PRODUTOS_DB_PATH = os.path.join(DB_DIR, "sistema.db")

class ListaProdutosDialog(QDialog):
    produto_selecionado = Signal(dict)

    def __init__(self, carrinho, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lista de Produtos")
        self.setGeometry(100, 100, 800, 600)
        self.carrinho = []

        # Layout principal
        self.layout = QHBoxLayout(self)

        # Tabela de produtos
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(5)
        self.tabela_produtos.setHorizontalHeaderLabels(["Nome do Produto", "Preço de Venda", "Categoria", "Estoque", "Ação"])
        self.tabela_produtos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.tabela_produtos)

        # Área à direita para filtros e produtos adicionados
        self.area_direita = QFrame(self)
        self.area_direita.setLayout(QVBoxLayout())
        self.layout.addWidget(self.area_direita)

        # Área de filtros de categoria
        self.filtros_layout = QGridLayout()
        self.area_direita.layout().addLayout(self.filtros_layout)

        # Carregar categorias e adicionar botões de filtro
        self.carregar_categorias()

        # Título
        self.titulo_label = QLabel("Produtos Adicionados")
        self.titulo_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.area_direita.layout().addWidget(self.titulo_label)

        # Lista de produtos adicionados
        self.produtos_adicionados_label = QLabel("Nenhum produto adicionado.")
        self.area_direita.layout().addWidget(self.produtos_adicionados_label)

        # Valor total
        self.total_label = QLabel("Valor Total: R$ 0.00")
        self.area_direita.layout().addWidget(self.total_label)

        # Botão para adicionar produtos ao pedido
        self.adicionar_button = QPushButton("Adicionar ao Pedido")
        self.adicionar_button.clicked.connect(self.adicionar_ao_pedido)
        self.area_direita.layout().addWidget(self.adicionar_button)

        # Carregar produtos do banco de dados
        self.carregar_produtos()

    def carregar_produtos(self, categoria=None):
        """Carrega produtos do banco de dados e exibe na tabela."""
        try:
            conn = sqlite3.connect(PRODUTOS_DB_PATH)
            cursor = conn.cursor()
            if categoria:
                cursor.execute("SELECT name, sale_price, category, stock_quantity FROM Products WHERE category = ?", (categoria,))
            else:
                cursor.execute("SELECT name, sale_price, category, stock_quantity FROM Products")
            produtos = cursor.fetchall()
            conn.close()

            self.tabela_produtos.setRowCount(0)  # Limpa a tabela antes de adicionar novos produtos

            for name, sale_price, category, stock_quantity in produtos:
                row_position = self.tabela_produtos.rowCount()
                self.tabela_produtos.insertRow(row_position)

                # Preenche as colunas
                self.tabela_produtos.setItem(row_position, 0, QTableWidgetItem(name))
                self.tabela_produtos.setItem(row_position, 1, QTableWidgetItem(f"R$ {sale_price:.2f}"))
                self.tabela_produtos.setItem(row_position, 2, QTableWidgetItem(category))
                self.tabela_produtos.setItem(row_position, 3, QTableWidgetItem(str(stock_quantity)))

                # Botão de adicionar
                add_button = QPushButton("Adicionar")
                add_button.clicked.connect(lambda checked, n=name, p=sale_price, s=stock_quantity: self.selecionar_quantidade(n, p, s))
                self.tabela_produtos.setCellWidget(row_position, 4, add_button)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar produtos: {e}")

    def carregar_categorias(self):
        """Carrega categorias do banco de dados e cria botões de filtro."""
        try:
            conn = sqlite3.connect(PRODUTOS_DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM Products")
            categorias = cursor.fetchall()
            conn.close()

            # Adiciona botões de filtro
            for i, (categoria,) in enumerate(categorias):
                button = QPushButton(categoria)
                button.clicked.connect(lambda checked, c=categoria: self.carregar_produtos(c))
                self.filtros_layout.addWidget(button, i // 3, i % 3)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar categorias: {e}")

    def selecionar_quantidade(self, name, sale_price, stock_quantity):
        """Solicita ao usuário a quantidade de produto a ser adicionada ao carrinho."""
        quantity_dialog = QDialog(self)
        quantity_dialog.setWindowTitle("Selecionar Quantidade")
        layout = QVBoxLayout(quantity_dialog)

        # SpinBox para selecionar a quantidade
        quantity_label = QLabel(f"Quantidade de {name}:")
        layout.addWidget(quantity_label)

        quantity_spinbox = QSpinBox()
        quantity_spinbox.setMinimum(1)
        quantity_spinbox.setMaximum(stock_quantity)
        layout.addWidget(quantity_spinbox)

        # Botão para confirmar a quantidade
        confirm_button = QPushButton("Confirmar")
        confirm_button.clicked.connect(lambda: self.adicionar_produto(name, sale_price, quantity_spinbox.value(), quantity_dialog))
        layout.addWidget(confirm_button)

        quantity_dialog.setLayout(layout)
        quantity_dialog.exec_()

    def adicionar_produto(self, name, sale_price, quantity, dialog):
        """Adiciona o produto selecionado ao carrinho."""
        produto = {'name': name, 'price': sale_price, 'quantity': quantity}
        self.carrinho.append(produto)  # Adiciona ao carrinho
        self.atualizar_produtos_adicionados()
        dialog.accept()  # Fecha o diálogo de quantidade
        QMessageBox.information(self, "Produto Adicionado", f"{name} foi adicionado ao carrinho.")

    def atualizar_produtos_adicionados(self):
        """Atualiza a lista de produtos adicionados e o valor total."""
        if not self.carrinho:
            self.produtos_adicionados_label.setText("Nenhum produto adicionado.")
            self.total_label.setText("Valor Total: R$ 0.00")
            return

        produtos_texto = ""
        total = 0

        for item in self.carrinho:
            produtos_texto += f"{item['name']} (R$ {item['price']:.2f} x {item['quantity']})\n"
            total += item['price'] * item['quantity']

        self.produtos_adicionados_label.setText(produtos_texto.strip())
        self.total_label.setText(f"Valor Total: R$ {total:.2f}")

    def adicionar_ao_pedido(self):
        for produto in self.carrinho:
            self.produto_selecionado.emit(produto)
        QMessageBox.information(self, "Produtos Adicionados", "Produtos foram adicionados ao pedido.")
        self.carrinho.clear()
        self.atualizar_produtos_adicionados()
        self.close()

class CarrinhoDialog(QDialog):
    def __init__(self, carrinho, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Carrinho de Compras")
        self.setGeometry(100, 100, 400, 300)
        self.carrinho = carrinho  # Recebe o carrinho de compras

        # Layout principal
        self.layout = QVBoxLayout(self)

        # Tabela de itens do carrinho
        self.atualizar_carrinho()

        # Botão para finalizar pedido
        finalize_button = QPushButton("Finalizar Pedido")
        finalize_button.clicked.connect(self.finalizar_pedido)
        self.layout.addWidget(finalize_button)

    def atualizar_carrinho(self):
        """Atualiza a lista de produtos no carrinho."""
        # Limpa o layout atual
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        total = 0
        for item in self.carrinho:
            frame = QFrame(self)
            layout = QHBoxLayout(frame)

            # Exibe informações do produto
            name_label = QLabel(item['name'])
            layout.addWidget(name_label)

            quantity_label = QLabel(f"Quantidade: {item['quantity']}")
            layout.addWidget(quantity_label)

            total_price = item['price'] * item['quantity']
            total += total_price
            total_label = QLabel(f"Total: R$ {total_price:.2f}")
            layout.addWidget(total_label)

            # Botão de remover
            remove_button = QPushButton("Remover")
            remove_button.clicked.connect(lambda checked, n=item['name']: self.remover_produto(n))
            layout.addWidget(remove_button)

            self.layout.addWidget(frame)

        total_label = QLabel(f"Total do Pedido: R$ {total:.2f}")
        self.layout.addWidget(total_label)

    def remover_produto(self, name):
        """Remove o produto do carrinho."""
        self.carrinho = [item for item in self.carrinho if item['name'] != name]
        self.atualizar_carrinho()

    def finalizar_pedido(self):
        """Finaliza o pedido."""
        if not self.carrinho:
            QMessageBox.warning(self, "Carrinho Vazio", "Não há produtos no carrinho!")
            return

        # Aqui, você pode implementar a lógica para processar o pedido
        QMessageBox.information(self, "Pedido Finalizado", "Seu pedido foi finalizado com sucesso!")

class MainApp(QApplication):
    def __init__(self, sys_argv):
        super(MainApp, self).__init__(sys_argv)
        self.carrinho = []  # Inicializa o carrinho de compras
        self.lista_produtos_dialog = ListaProdutosDialog(self.carrinho)
        self.lista_produtos_dialog.produto_selecionado.connect(self.adicionar_item)
        self.lista_produtos_dialog.exec_()

        # Após adicionar produtos, você pode abrir o carrinho
        self.carrinho_dialog = CarrinhoDialog(self.carrinho)
        self.carrinho_dialog.exec_()

    def adicionar_item(self, produto):
        # Lógica para adicionar o produto ao pedido
        print(f"Produto adicionado ao pedido: {produto}")

if __name__ == "__main__":
    import sys
    app = MainApp(sys.argv)
    sys.exit(app.exec())