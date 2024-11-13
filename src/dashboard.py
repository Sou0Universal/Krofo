import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTabWidget, QHBoxLayout, QGridLayout,
    QMessageBox, QGroupBox, QFrame
)
from PySide6.QtCore import QTimer, Qt, QDateTime, QSize
from PySide6.QtGui import QIcon, QPixmap
from .utils import load_stylesheet, load_dark_stylesheet
from .abrir_caixa import AbrirCaixaWidget
from .fechar_caixa import FecharCaixaWidget
from .database import init_db
from .historico import HistoricoFechamentosDialog
from .Entrada_Saida import EntradaSaidaWindow
from .button_config import get_button_data
from .widgets import AnimatedButton
from .save import save_state, load_state
from src.importar_produtos import ImportarProdutosWidget
from src.adicionar_pedido import AdicionarPedidoWidget


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        state = load_state()
        self.restore_state(state)
        self.total_entradas = 0.0
        self.total_saidas = 0.0

    def setup_ui(self):
        self.setWindowTitle("Dashboard de Fluxo de Caixa")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('1.jpg'))
        self.setStyleSheet(load_stylesheet())

        init_db()

        self.dark_mode = False
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.create_top_navigation()

        self.button_group = self.create_button_group()
        self.main_layout.addWidget(self.button_group)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tab_widget)

        self.clock_label = QLabel()
        self.main_layout.addWidget(self.clock_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

        self.caixa_aberto = False

        self.update_buttons("PRINCIPAL")

    def create_top_navigation(self):
        navigation_layout = QHBoxLayout()
        sections = ["PRINCIPAL", "PRODUTOS", "FINANCEIRO", "CONFIGURAÇÕES", "APPS"]

        for section in sections:
            button = AnimatedButton(section)
            button.setObjectName("nav-li")
            button.setCheckable(True)
            button.clicked.connect(lambda checked, sec=section: self.update_active_nav(sec))
            navigation_layout.addWidget(button)

            if section != sections[-1]:
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setObjectName("nav-line")
                navigation_layout.addWidget(line)

        self.main_layout.addLayout(navigation_layout)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet(load_dark_stylesheet())
        else:
            self.setStyleSheet(load_stylesheet())

    def create_button_group(self):
        button_group = QGroupBox("Menu de Funções")
        button_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid gray;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
        """)
        self.button_layout = QGridLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)
        button_group.setLayout(self.button_layout)
        return button_group

    def update_active_nav(self, section):
        for i in range(self.main_layout.itemAt(0).layout().count()):
            widget = self.main_layout.itemAt(0).layout().itemAt(i).widget()
            if isinstance(widget, AnimatedButton):
                widget.setChecked(False)

        button = self.sender()
        if button:
            button.setChecked(True)

        self.update_buttons(section)

    def update_clock(self):
        self.clock_label.setText(QDateTime.currentDateTime().toString("hh:mm:ss"))

    def update_buttons(self, section):
        for i in reversed(range(self.button_layout.count())):
            widget = self.button_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        button_data = get_button_data()

        for index, (text, icon, callback_name, button_name, *args) in enumerate(button_data.get(section, [])):
            self.create_button(text, icon, callback_name, button_name, args, index)

    def create_button(self, text, icon, callback_name, button_name, args, index):
        button = AnimatedButton("")
        button.setObjectName(button_name)
        button.setFixedSize(100, 100)
        self.set_button_icon(button, icon)

        if args:
            button.clicked.connect(lambda checked, cb=callback_name, a=args[0]: getattr(self, cb)(a))
        else:
            button.clicked.connect(getattr(self, callback_name))

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(button)
        vbox.addWidget(label)
        vbox.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container.setLayout(vbox)

        self.button_layout.addWidget(container, 0, index)

    def set_button_icon(self, button, icon_path):
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Erro", f"Ícone '{icon_path}' não encontrado.")
        button.setIcon(QIcon(pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        button.setIconSize(QSize(75, 75))

    def handle_caixa(self):
        if not self.caixa_aberto:
            self.open_abrir_caixa()
        else:
            self.open_fechar_caixa()
            
    def open_tab(self, tab_name, widget=None):
        existing_tabs = [self.tab_widget.tabText(i) for i in range(self.tab_widget.count())]
        if tab_name not in existing_tabs:
            new_tab = QWidget()
            layout = QVBoxLayout()

            if widget is not None:
                layout.addWidget(widget)           
            if tab_name == "Abertura de Caixa":
                widget = AbrirCaixaWidget(self.fechar_caixa_callback)
                layout.addWidget(widget)
            elif tab_name == "Fechamento de Caixa":
                widget = FecharCaixaWidget(self, self.finalizar_caixa_callback)
                layout.addWidget(widget)
            elif tab_name == "Entradas e Saídas":
                self.entrada_saida_widget = EntradaSaidaWindow(close_callback=lambda: self.close_tab_with_name(tab_name))
                layout.addWidget(self.entrada_saida_widget)
            elif tab_name == "Histórico de Fechamentos":
                widget = HistoricoFechamentosDialog()
                layout.addWidget(widget)
            else:
                layout.addWidget(QLabel(f"Conteúdo da aba {tab_name}"))

            new_tab.setLayout(layout)
            self.tab_widget.addTab(new_tab, tab_name)
        
        self.tab_widget.setCurrentIndex(existing_tabs.index(tab_name) if tab_name in existing_tabs else self.tab_widget.count() - 1)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def open_abrir_caixa(self):
        self.open_tab("Abertura de Caixa")

    def fechar_caixa_callback(self, saldo_numerico, observacao):
        self.caixa_aberto = True
        self.tab_widget.removeTab(self.tab_widget.currentIndex())
        self.open_fechar_caixa()

    def open_fechar_caixa(self):
        self.open_tab("Fechamento de Caixa")

    def finalizar_caixa_callback(self, *args):
        self.caixa_aberto = False
        self.tab_widget.removeTab(self.tab_widget.currentIndex())

    def open_entrada_saida(self):
        self.open_tab("Entradas e Saídas")

    def close_tab_with_name(self, tab_name):
        for index in range(self.tab_widget.count()):
            if self.tab_widget.tabText(index) == tab_name:
                self.tab_widget.removeTab(index)
                break

    def open_historico(self):
        self.open_tab("Histórico de Fechamentos")

    def restore_state(self, state):
        open_tabs = state.get('open_tabs', [])
        for tab_name in open_tabs:
            self.open_tab(tab_name)

    def get_current_state(self):
        state = {
            'open_tabs': [self.tab_widget.tabText(i) for i in range(self.tab_widget.count())]
        }
        return state

    def closeEvent(self, event):
        state = self.get_current_state()
        save_state(state)
        event.accept()

    def get_total_entradas(self):
        return self.total_entradas

    def get_total_saidas(self):
        return self.total_saidas

    def get_daily_totals(self):
        entrada_saida_window = EntradaSaidaWindow()
        return entrada_saida_window.get_daily_totals()
    
    def adicionar_transacao(self, tipo, valor):
        if tipo == "entrada":
            self.total_entradas += valor
        elif tipo == "saida":
            self.total_saidas += valor  # Corrigido para somar saídas
        self.atualizar_interface_caixa()

    def produtos_callback(self):
        self.importar_produtos_widget = ImportarProdutosWidget()
        self.importar_produtos_widget.show()

    def complementos_callback(self):
        self.open_tab("Complementos")

    def observacoes_callback(self):
        self.open_tab("Observações")

    def categorias_callback(self):
        self.open_tab("Categorias")

    def tipos_tamanhos_callback(self):
        self.open_tab("Tipos e Tamanhos")

    def perguntas_callback(self):
        self.open_tab("Perguntas")

    def insumos_callback(self):
        self.open_tab("Insumos")

    def alterar_estoque_lote_callback(self):
        self.open_tab("Alterar Estoque em Lote")

    def alterar_estoque_nfe_callback(self):
        self.open_tab("Alterar Estoque com NFe")

    def historico_entradas_saidas_callback(self):
        self.open_tab("Histórico de Entradas e Saídas")

    def posicao_data_callback(self):
        self.open_tab("Posição por Data")

    def promocoes_callback(self):
        self.open_tab("Promoções")

    def historico_itens_vendidos_callback(self):
        self.open_tab("Histórico de Itens Vendidos")

    def open_adicionar_pedido(self):
        if not self.caixa_aberto: 
            QMessageBox.warning(self, "Atenção", "O caixa deve estar aberto para adicionar pedidos.")
            return 
        
        widget = AdicionarPedidoWidget()
        widget.set_callback(self.adicionar_transacao)
        self.open_tab("Adicionar Pedido", widget) 
        
    def close_app(self):
        self.close()
        
    def atualizar_interface_caixa(self):
        if hasattr(self, 'entrada_saida_widget'):
            self.entrada_saida_widget.update_totals(self.total_entradas, self.total_saidas)
            
    def fechar_caixa_callback(self, saldo_numerico, observacao):
     self.caixa_aberto = True 
     self.tab_widget.removeTab(self.tab_widget.currentIndex())
     self.open_fechar_caixa()

    def abrir_caixa_callback(self):
     self.caixa_aberto = True  