from PySide6.QtWidgets import QHBoxLayout, QFrame
from .widgets import AnimatedButton

def create_top_navigation(parent, update_active_nav):
    navigation_layout = QHBoxLayout()
    sections = ["PRINCIPAL", "PRODUTOS", "FINANCEIRO", "CONFIGURAÇÕES", "APPS"]

    for section in sections:
        button = AnimatedButton(section)
        button.setObjectName("nav-li")
        button.setCheckable(True)
        button.clicked.connect(lambda checked, sec=section: update_active_nav(sec))
        navigation_layout.addWidget(button)

        if section != sections[-1]:
            line = QFrame()
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setObjectName("nav-line")
            navigation_layout.addWidget(line)

    parent.main_layout.addLayout(navigation_layout)