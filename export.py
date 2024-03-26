import sqlite3
import csv

def export_summary_to_csv():
    conn = sqlite3.connect('ear.db')
    c = conn.cursor()

    c.execute("SELECT category, SUM(amount) FROM credit_card_transactions GROUP BY category")
    expenses = c.fetchall()

    filename = input("Geben Sie den Dateinamen für die CSV-Datei ein (ohne Erweiterung): ")
    filename += ".csv"
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Kategorie', 'Gesamtausgaben'])
        for expense in expenses:
            csvwriter.writerow(expense)

    print(f"Die Zusammenfassung wurde erfolgreich in '{filename}' exportiert.")

    conn.close()

if __name__ == "__main__":
    export_summary_to_csv()
