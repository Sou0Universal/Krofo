# src/utils.py
import os


def validate_username(username):
    if len(username) < 3:
        return False
    return True

def validate_password(password):
    if len(password) < 6:
        return False
    return True

def load_stylesheet():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_path, "r") as file:
        return file.read()
    
def load_dark_stylesheet():
    return """
    QWidget {
        background-color: #2e2e2e;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: 1px solid #444444;
    }
    QPushButton#button-caixa {
        background-color: #4A90E2; /* Azul para confiança e segurança */
    }
    QPushButton#button-historico {
        background-color: #FF8A65; /* Laranja para dinamismo */
    }
    QPushButton#button-relatorios {
        background-color: #4DB6AC; /* Turquesa para equilíbrio */
    }
    QPushButton#button-alertas {
        background-color: #E57373; /* Vermelho suave para atenção */
    }
    QPushButton#button-orcamento {
        background-color: #FFD54F; /* Amarelo suave para otimismo */
    }
    QPushButton#button-import {
        background-color: #BA68C8; /* Roxo para criatividade */
    }
    QPushButton#button-relatorio-fechamento {
        background-color: #81C784; /* Verde para renovação */
    }
    QPushButton#button-sair {
        background-color: #F06292; /* Rosa para urgência */
    }
    QPushButton:hover {
        background-color: #5C6BC0; /* Azul violeta para destaque */
        color: #ffffff;
    }
    QPushButton#nav-li {
        background-color: #4A90E2;
        color: white;
        border: none;
        min-width: 100%; 
        height: 20px; 
        font-size: 12px;
    }
    QTabBar::tab {
        background-color: #4A90E2;
        color: #ffffff;
        padding: 10px;
    }
    #abrirCaixaButton {
        background-color: #7986CB;
        color: #ffffff;
        border: 1px solid #5C6BC0; 
        border-radius: 5px;
        padding: 5px 10px;
    }
    #abrirCaixaButton:hover {
        background-color: #3f89b4bd;
    }
    #abrirCaixaButton:pressed {
        background-color: #c0c0c0;
    }
    #entradaSaidaButton {
        background-color: #FFD54F;
        color: #000000;
        border: 1px solid #aaaaaa;
        border-radius: 5px;
        padding: 5px 10px;
    }
    #entradaSaidaButton:hover {
        background-color: #3f89b4bd;
    }
    #entradaSaidaButton:pressed {
        background-color: #c0c0c0;
    }
    #fecharCaixaButton {
        background-color: #F06292;
        color: #000000;
        border: 1px solid #aaaaaa;
        border-radius: 5px;
        padding: 5px 10px;
    }
    #fecharCaixaButton:hover {
        background-color: #3f89b4bd;
    }
    #fecharCaixaButton:pressed {
        background-color: #c0c0c0;
    }
    QLineEdit, QTextEdit, QDateEdit {
        background-color: #424242;
        border: 1px solid #5C6BC0;
        border-radius: 5px;
        padding: 3px;
        color: #ffffff;
    }
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #ffffff;
    }
    QTableView::section {
    background-color: #4A90E2; /* Cor dos cabeçalhos */
    color: #ffffff; /* Cor do texto nos cabeçalhos */
    border: 1px solid #ccc;
    padding: 5px;
    font-weight: bold;
}

QTableView {
    gridline-color: #ccc; /* Cor das linhas */
}

QHeaderView::section {
    background-color: #4A90E2; /* Mesma cor dos cabeçalhos */
    color: #ffffff;
    padding: 5px;
    font-weight: bold;
}

QTableView::item {
    color: #ffffff;; /* Cor do texto padrão */
}

/* Botões específicos */
QPushButton#button-caixa {
    background-color: #4A90E2; /* Azul para confiança */
}

QPushButton#button-adicionar-pedido {
    background-color: #ffffff; /* Branco intenso para paz */
}

QPushButton#button-historico {
    background-color: #F57C00; /* Laranja intenso para energia */
}

QPushButton#button-relatorios {
    background-color: #66BB6A; /* Verde suave para equilíbrio */
}

QPushButton#button-alertas {
    background-color: #FF7043; /* Vermelho suave para atenção */
}

QPushButton#button-orcamento {
    background-color: #FFEB3B; /* Amarelo vibrante para otimismo */
}

QPushButton#button-import {
    background-color: #29B6F6; /* Azul claro para tranquilidade */
}

QPushButton#button-relatorio-fechamento {
    background-color: #8BC34A; /* Verde claro para renovação */
}

QPushButton#button-sair {
    background-color: #E91E63; /* Rosa para urgência */
}

QPushButton:hover {
    background-color: #7E57C2; /* Roxo para destaque */
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #5E35B1; /* Roxo escuro ao clicar */
    color: #ffffff;
}

#produtos_button {
    background-color: #FF5733; /* Orange */
    color: white;
}

#complementos_button {
    background-color: #33FF57; /* Green */
    color: white;
}

#observacoes_button {
    background-color: #3357FF; /* Blue */
    color: white;
}

#categorias_button {
    background-color: #FF33FF; /* Pink */
    color: white;
}

#tipos_tamanhos_button {
    background-color: #FF8C33; /* Coral */
    color: white;
}

#perguntas_button {
    background-color: #33FFF5; /* Aqua */
    color: white;
}

#insumos_button {
    background-color: #8C33FF; /* Purple */
    color: white;
}

#alterar_estoque_lote_button {
    background-color: #FF3333; /* Red */
    color: white;
}

#alterar_estoque_nfe_button {
    background-color: #33FF99; /* Light Green */
    color: white;
}

#historico_entradas_saidas_button {
    background-color: #FF9933; /* Amber */
    color: white;
}

#posicao_data_button {
    background-color: #3399FF; /* Light Blue */
    color: white;
}

#promocoes_button {
    background-color: #FF33CC; /* Magenta */
    color: white;
}

#historico_itens_vendidos_button {
    background-color: #99FF33; /* Lime */
    color: white;
}

/* FINANCEIRO (9-16) */
QPushButton#button-financeiro-9 {
    background-color: #F57C00; /* Laranja intenso para energia */
}

QPushButton#button-financeiro-10 {
    background-color: #8BC34A; /* Verde claro para renovação */
}

QPushButton#button-financeiro-11 {
    background-color: #4A90E2; /* Azul para confiança */
}

QPushButton#button-financeiro-12 {
    background-color: #FF7043; /* Vermelho suave para atenção */
}

QPushButton#button-financeiro-13 {
    background-color: #29B6F6; /* Azul claro para tranquilidade */
}

QPushButton#button-financeiro-14 {
    background-color: #FFEB3B; /* Amarelo vibrante para otimismo */
}

QPushButton#button-financeiro-15 {
    background-color: #E91E63; /* Rosa para urgência */
}

QPushButton#button-financeiro-16 {
    background-color: #66BB6A; /* Verde suave para equilíbrio */
}

/* CONFIGURAÇÕES (17-24) */
QPushButton#button-config-dark {
    background-color: #66BB6A; /* Verde suave para equilíbrio */
}

QPushButton#button-config-18 {
    background-color: #E91E63; /* Rosa para urgência */
}

QPushButton#button-config-19 {
    background-color: #FFEB3B; /* Amarelo vibrante para otimismo */
}

QPushButton#button-config-20 {
    background-color: #F57C00; /* Laranja intenso para energia */
}

QPushButton#button-config-21 {
    background-color: #8BC34A; /* Verde claro para renovação */
}

QPushButton#button-config-22 {
    background-color: #29B6F6; /* Azul claro para tranquilidade */
}

QPushButton#button-config-23 {
    background-color: #4A90E2; /* Azul para confiança */
}

QPushButton#button-config-24 {
    background-color: #FF7043; /* Vermelho suave para atenção */
}

/* APPS (25-32) */
QPushButton#button-app-25 {
    background-color: #29B6F6; /* Azul claro para tranquilidade */
}

QPushButton#button-app-26 {
    background-color: #FFEB3B; /* Amarelo vibrante para otimismo */
}

QPushButton#button-app-27 {
    background-color: #F57C00; /* Laranja intenso para energia */
}

QPushButton#button-app-28 {
    background-color: #8BC34A; /* Verde claro para renovação */
}

QPushButton#button-app-29 {
    background-color: #E91E63; /* Rosa para urgência */
}

QPushButton#button-app-30 {
    background-color: #66BB6A; /* Verde suave para equilíbrio */
}

QPushButton#button-app-31 {
    background-color: #FF7043; /* Vermelho suave para atenção */
}

QPushButton#button-app-32 {
    background-color: #4A90E2; /* Azul para confiança */
}

    """