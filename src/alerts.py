# src/alerts.py

class Alerts:
    def __init__(self):
        self.notifications = []

    def add_notification(self, message):
        self.notifications.append(message)

    def check_alerts(self, transactions):
        """Verifica se há alertas, como saldo baixo."""
        # Implementar lógica de alertas
        pass

    def get_notifications(self):
        return self.notifications