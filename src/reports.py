# src/reports.py

import sqlite3

class Reports:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def get_monthly_report(self, month, year):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT SUM(amount) FROM transactions
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        ''', (month, year))
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def close(self):
        self.connection.close()