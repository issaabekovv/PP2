import psycopg2
from connect import get_connection, create_tables

def add_or_update(name, phone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
    print("Done")

def bulk_insert():
    # Пример данных для массовой вставки
    names = ["Alice", "Bob", "Charlie", "WrongNum"]
    phones = ["77011112233", "77022223344", "77055556677", "123"] # Последний не пройдет валидацию
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))
        conn.commit()
    print("Bulk insert executed (check notices for errors)")

def search(pattern):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts_fn(%s)", (pattern,))
            results = cur.fetchall()
            for r in results:
                print(f"{r[0]} | {r[1]} | {r[2]}")

def get_page(limit, offset):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            for r in cur.fetchall():
                print(f"{r[0]} | {r[1]} | {r[2]}")

def delete(val):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact_proc(%s)", (val,))
        conn.commit()
    print("Deleted")

def main():
    create_tables()
    while True:
        print("\n1. Add/Update\n2. Bulk Insert (Example)\n3. Search\n4. Pagination\n5. Delete\n0. Exit")
        choice = input("> ")

        if choice == '1':
            add_or_update(input("Name: "), input("Phone: "))
        elif choice == '2':
            bulk_insert()
        elif choice == '3':
            search(input("Pattern: "))
        elif choice == '4':
            l = int(input("Limit: "))
            o = int(input("Offset: "))
            get_page(l, o)
        elif choice == '5':
            delete(input("Name/Phone: "))
        elif choice == '0':
            break

if __name__ == "__main__":
    main()