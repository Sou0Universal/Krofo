import sqlite3
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel, QMessageBox, QTextEdit

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "transactions.db")

class DetalhesFechamentoDialog(QDialog):
    def __init__(self, row_data):
        super().__init__()
        self.setWindowTitle("Detalhes do Fechamento")
        layout = QVBoxLayout(self)

        date, closing_value, opening_value, total_entries, total_exits, observations = row_data

        # Informações do fechamento
        info_label = QLabel(
            f"<b>Data:</b> {date}<br>"
            f"<b>Valor de Abertura:</b> R${opening_value:.2f}<br>"
            f"<b>Saldo Final:</b> R${closing_value:.2f}<br>"
            f"<b>Total de Entradas:</b> R${total_entries:.2f}<br>"
            f"<b>Total de Saídas:</b> R${total_exits:.2f}<br>"
        )
        layout.addWidget(info_label)

        # Detalhes das transações
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        layout.addWidget(self.details_text)

        self.load_transaction_details(date)

    def load_transaction_details(self, date):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Obter transações para a data especificada
        cursor.execute("SELECT date, type, amount, note FROM transactions WHERE date LIKE ? ORDER BY date", (f"{date}%",))
        transactions = cursor.fetchall()
        connection.close()

        # Formatar detalhes das transações
        details = []
        entradas = []
        saidas = []
        
        for date_time, tipo, amount, note in transactions:
            tipo_str = "Entrada" if tipo == "entrada" else "Saída"
            formatted = f"{date_time} - R${amount:.2f} - {tipo_str}"
            if note:
                formatted += f" - {note}"

            if tipo == "entrada":
                entradas.append(formatted)
            else:
                saidas.append(formatted)

        # Adicionar ao texto
        if entradas:
            details.append("<b>Entradas:</b>")
            details.extend(entradas)
        if saidas:
            details.append("<b>Saídas:</b>")
            details.extend(saidas)

        self.details_text.setText("\n".join(details))

class HistoricoFechamentosDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histórico de Fechamentos")
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Data", "Valor Final", "Detalhes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.clear_button = QPushButton("Limpar Histórico")
        self.clear_button.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_button)

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT date, closing_value, opening_value, total_entries, total_exits, observations FROM close_registers WHERE closing_value IS NOT NULL")
        records = cursor.fetchall()
        connection.close()

        self.table.setRowCount(len(records))

        for row_index, row_data in enumerate(records):
            date_item = QTableWidgetItem(row_data[0])
            final_value_item = QTableWidgetItem(f"R${row_data[1]:.2f}")
            details_button = QPushButton("Ver Detalhes")
            details_button.clicked.connect(lambda checked, row=row_data: self.show_details(row))
            self.table.setItem(row_index, 0, date_item)
            self.table.setItem(row_index, 1, final_value_item)
            self.table.setCellWidget(row_index, 2, details_button)

    def show_details(self, row_data):
        detalhes_dialog = DetalhesFechamentoDialog(row_data)
        detalhes_dialog.exec()

    def clear_history(self):
        confirmation = QMessageBox.question(self, "Confirmar Limpeza", "Tem certeza de que deseja limpar o histórico?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM close_registers")
            connection.commit()
            connection.close()

            self.load_data()
            QMessageBox.information(self, "Histórico Limpo", "O histórico foi limpo com sucesso.")