import sqlite3
from datetime import datetime
import csv

conn = sqlite3.connect('ear.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS credit_card_transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        description TEXT,
        category TEXT, 
        date DATE
    )
''')

conn.commit()

def add_credit_card_transaction(amount, description, category):
    date_choice = input("Datum eingeben (YYYY-MM-DD) oder Enter drücken für das heutige Datum: ")
    if date_choice:
        date = date_choice
    else:
        date = datetime.now().strftime('%Y-%m-%d')

    c.execute('INSERT INTO credit_card_transactions(amount, description, category, date) VALUES (?,?,?,?)',
              (amount, description, category, date))
    conn.commit()
    print("Credit card transaction added successfully!") 

def export_transactions_to_csv(transactions):
    filename = input("Geben Sie den Dateinamen für die CSV-Datei ein (ohne Erweiterung): ")
    filename += ".csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Betrag', 'Beschreibung', 'Kategorie', 'Datum'])
        for transaction in transactions:
            csvwriter.writerow(transaction)


def view_credit_card_transactions():
    c.execute("SELECT * FROM credit_card_transactions ORDER BY date")
    transactions = c.fetchall()
    
    if transactions:
        print("Nr.   / Betrag  / Beschreibung    / Kategorie      / Datum ")
        print("_____________________________________________________________")
        for transaction in transactions:
            print(f"{transaction[0]:<3}  / €{transaction[1]:<7.2f}  / {transaction[2]:<27}  / {transaction[3]:<14} / {transaction[4]}")
    else:
        print("No credit card transactions found")

def add_income(amount, description):
    date = datetime.now().strftime('%Y-%m-%d')
    c.execute('INSERT INTO credit_card_transactions(amount, description, date) VALUES (?,?,?)',
              (amount, description, date))
    conn.commit()
    print("Income added successfully!") 
def calculate_monthly_expenses():
    c.execute("SELECT category, SUM(amount) FROM credit_card_transactions GROUP BY category")
    expenses = c.fetchall()
    
    total_expenses = 0  # Variable zur Berechnung der Gesamtsumme der Ausgaben
    
    if expenses:
        print("Kategorie      / Gesamtausgaben ")
        print("________________________________")
        for expense in expenses:
            print(f"{expense[0]:<14} / €{expense[1]:.2f}")
            total_expenses += expense[1]  # Summiere den Betrag für jede Kategorie
        
        print(f"\nGesamtsumme: €{total_expenses:.2f}")  # Ausgabe der Gesamtsumme
    else:
        print("Keine Ausgaben gefunden")
    

def main():
    while True:
        print("\nEAR - Kreditkartenabrechnung")
        print("1. Transaktion hinzufügen")
        print("2. Verlauf anschauen")
        print("3. Einnahme hinzufügen")
        print("4. Monatliche Ausgaben berechnen")
        print("5. Verlassen")
        print("6. Mindestzahlung und Fälligkeitsdatum anzeigen")
        
        choice = input("Auswählen: ")
        if choice == '1':
            amount = float(input("Betrag: "))
            description = input("Beschreibung: ")
            category = input("Kategorie: ")
            add_credit_card_transaction(amount, description, category)
            
        elif choice == "2":   
            view_credit_card_transactions()
            
        elif choice == '3':
            amount = float(input("Betrag: "))
            description = input("Beschreibung: ")
            add_income(amount, description)
        
        elif choice == '4':
            calculate_monthly_expenses()
            from export import export_summary_to_csv
            export_summary_to_csv()

            
        elif choice == '5':
            print("Verlassen...\n")
            break
        
        elif choice == '6':
            from payment_reminder import calculate_payment_due_date
            calculate_payment_due_date()


if __name__ == "__main__":
    main()
    
conn.close()
