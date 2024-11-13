# src/app.py

from PySide6.QtWidgets import QMainWindow
from .login import LoginWindow

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meu Aplicativo")
        self.setGeometry(100, 100, 800, 600)

        # Inicializa a janela de login
        self.login_window = LoginWindow(self)
        self.setCentralWidget(self.login_window)  # Mostra a janela de login como central