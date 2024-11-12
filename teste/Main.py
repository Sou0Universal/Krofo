import sys
from PySide6 import QtWidgets
from src.dashboard import DashboardWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dashboard_app = DashboardWindow()
    dashboard_app.show()
    sys.exit(app.exec())