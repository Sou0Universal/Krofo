from PySide6.QtWidgets import QPushButton

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setStyleSheet(self.styleSheet() + "background-color: #b2dfdbab;color: #333;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("")
        super().leaveEvent(event)