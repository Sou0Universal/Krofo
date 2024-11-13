# src/models.py

class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

class Transaction:
    def __init__(self, transaction_id, description, amount, date, transaction_type):
        self.transaction_id = transaction_id
        self.description = description
        self.amount = amount
        self.date = date
        self.transaction_type = transaction_type  # 'entrada' ou 'saida'

class CashRegister:
    def __init__(self, initial_amount, responsible):
        self.initial_amount = initial_amount
        self.responsible = responsible
        self.closing_balance = None