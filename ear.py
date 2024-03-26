from datetime import datetime
import sqlite3
import readline  # tab-completion 

conn = sqlite3.connect('ear.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date DATE
    )
''')

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

def add_expense(amount, category, description):
    date = datetime.now().strftime('%Y-%m-%d')
    c.execute('INSERT INTO expenses(amount, category, description, date) VALUES (?,?,?,?)',
              (amount, category, description, date))
    conn.commit()
    print("Expense added successfully!") 

def view_expenses():
    c.execute("SELECT * FROM expenses ORDER BY date")
    expenses = c.fetchall()
    
    if expenses:
        print("Nr.   / Betrag  / Kategorie  / Beschreibung    / Datum ")
        print("___________________________________________________________")
        for expense in expenses:
            print(f"{expense[0]:<3}  / €{expense[1]:<7.2f}  / {expense[2]:<15} / {expense[3]:<27}  / {expense[4]}")
    else:
        print("No expenses found")

def suggest_description(text, state):
    descriptions = ["Miete", "Versicherung", "Transport", "Mobilvertrag"]  # wiederkehrende Ausgaben
    
    if text:
        options = [desc for desc in descriptions if desc.startswith(text)]
    else:
        options = descriptions
    
    return options[state]

def main():
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(suggest_description)

    while True:
        print("\nEAR")
        print("1. Transaktion hinzufügen")
        print("2. Verlauf anschauen")
        print("3. Verlassen")
        
        choice = input("Auswählen: ")
        if choice == '1':
            amount = float(input("Betrag: "))
            category = input("Kategorie: ")
            description = input("Beschreibung: ")
            add_expense(amount, category, description)
            
        elif choice == "2":   
            view_expenses()
            
        elif choice == '3':
            print("Verlassen...\n")
            break   
        
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
    
conn.close()
