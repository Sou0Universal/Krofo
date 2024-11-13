from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox


class ImportExportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Importação/Exportação de Cardápios")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout(self)

        # Título
        title_label = QLabel("Importação/Exportação de Cardápios Virtuais")
        layout.addWidget(title_label)

        # Botão de Importação
        import_button = QPushButton("Importar Cardápio")
        import_button.clicked.connect(self.import_menu)
        layout.addWidget(import_button)
        import_button.setObjectName("importButton")

        # Botão de Exportação
        export_button = QPushButton("Exportar Cardápio")
        export_button.clicked.connect(self.export_menu)
        layout.addWidget(export_button)
        export_button.setObjectName("exportButton")

    def import_menu(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Importar Cardápio", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            # Adicione aqui a lógica para importar o cardápio
            QMessageBox.information(self, "Importação", f"Cardápio importado de {file_name}")

    def export_menu(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar Cardápio", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            # Adicione aqui a lógica para exportar o cardápio
            QMessageBox.information(self, "Exportação", f"Cardápio exportado para {file_name}")