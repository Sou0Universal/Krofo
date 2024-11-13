import sys
from PySide6.QtWidgets import QApplication
from src.dashboard import DashboardWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())