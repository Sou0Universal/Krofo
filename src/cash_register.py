class CashRegister:
    def __init__(self):
        self.balance = 0.0
        self.transactions = []

    def open_cash_register(self, amount):
        self.balance += amount
        self.transactions.append({"type": "entrada", "amount": amount})

    def add_transaction(self, description, amount, transaction_type):
        self.transactions.append({"description": description, "amount": amount, "type": transaction_type})
        if transaction_type == 'entrada':
            self.balance += amount
        elif transaction_type == 'saida':
            self.balance -= amount

    def close_cash_register(self):
        return self.balance