from datetime import datetime, timedelta
import sqlite3

def calculate_payment_due_date():
    conn = sqlite3.connect('ear.db')
    c = conn.cursor()

    # Annahme: Mindestzahlung ist 10% der gesamten Kreditkartenausgaben in diesem Monat
    c.execute("SELECT SUM(amount) FROM credit_card_transactions WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')")
    total_expenses = c.fetchone()[0] or 0
    minimum_payment = total_expenses * 0.1  # Mindestzahlung ist 10% der gesamten Ausgaben

    # Annahme: Fälligkeitsdatum ist 25 Tage nach Ende des aktuellen Monats
    current_date = datetime.now()
    last_day_of_month = current_date.replace(day=1, month=current_date.month+1) - timedelta(days=1)
    due_date = last_day_of_month + timedelta(days=25)  # Fälligkeitsdatum ist 25 Tage nach Ende des Monats

    days_until_due = (due_date - current_date).days

    print(f"Mindestzahlung: €{minimum_payment:.2f}")
    print(f"Fälligkeitsdatum: {due_date.strftime('%Y-%m-%d')}")
    print(f"{days_until_due} Tage bis zur nächsten Zahlung.")

    conn.close()

if __name__ == "__main__":
    calculate_payment_due_date()
