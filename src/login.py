# src/login.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .database import Database
from .dashboard import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Faça login:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome de usuário")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.handle_login)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        self.database = Database()
        if self.database.validate_user(username, password):
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")

            # Abre uma nova janela do dashboard
            self.dashboard = DashboardWindow()
            self.dashboard.show()  # Mostra a janela do dashboard

            # Fecha a janela de login
            self.parent().close()  # Fecha a janela central (App)
        else:
            QMessageBox.warning(self, "Erro", "Nome de usuário ou senha incorretos.")

        self.database.close()