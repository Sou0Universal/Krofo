from PySide6.QtCore import QTime

def update_clock(clock_label):
    current_time = QTime.currentTime().toString("hh:mm:ss")
    clock_label.setText(current_time)