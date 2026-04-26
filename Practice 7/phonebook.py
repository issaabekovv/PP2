import csv
from connect import get_connection, create_tables

def import_from_csv(filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        cur.execute(
                            "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            (row[0], row[1])
                        )
            print(f"Imported {filename}")
    except Exception as e:
        print(f"Error: {e}")

def add_contact(name, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
                print("Contact added")
    except Exception as e:
        print(f"Error: {e}")

def update_contact(name, new_phone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE contacts SET phone = %s WHERE name = %s", (new_phone, name))
            print("Contact updated")

def search_contacts(pattern):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contacts WHERE name ILIKE %s OR phone LIKE %s", 
                        (f"%{pattern}%", f"%{pattern}%"))
            for r in cur.fetchall():
                print(f"{r[0]} | {r[1]} | {r[2]}")

def delete_contact(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE name = %s OR phone = %s", (data, data))
            print("Deleted")

def main():
    create_tables()
    while True:
        print("\n1. Import CSV\n2. Add\n3. Search\n4. Update\n5. Delete\n0. Exit")
        choice = input("> ")

        if choice == '1':
            import_from_csv(input("File: "))
        elif choice == '2':
            add_contact(input("Name: "), input("Phone: "))
        elif choice == '3':
            search_contacts(input("Search: "))
        elif choice == '4':
            update_contact(input("Name: "), input("New phone: "))
        elif choice == '5':
            delete_contact(input("Name/Phone: "))
        elif choice == '0':
            break

if __name__ == "__main__":
    main()