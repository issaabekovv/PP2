import json
import csv
import os
from connect import get_connection

def search_extended():
    query_str = input("Search query: ")
    sql = """
        SELECT c.name, c.email, g.name, array_agg(p.phone) 
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.name ILIKE %s OR c.email ILIKE %s OR p.phone ILIKE %s
        GROUP BY c.id, g.name
    """
    pattern = f"%{query_str}%"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (pattern, pattern, pattern))
            for r in cur.fetchall():
                phones = ', '.join(filter(None, r[3])) if r[3] else "No numbers"
                print(f"{r[0]} | {r[1]} | {r[2]} | {phones}")

def filter_by_group():
    group_name = input("Enter group name to filter: ")
    sql = """
        SELECT c.name, c.email, g.name 
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (group_name,))
            rows = cur.fetchall()
            if not rows:
                print("No contacts found in this group.")
            for r in rows:
                print(f"{r[0]} | {r[1]} | Group: {r[2]}")

def export_to_json():
    sql = "SELECT id, name, email, birthday, group_id FROM contacts"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            contacts = cur.fetchall()
            data = []
            for c in contacts:
                cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (c[0],))
                phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
                cur.execute("SELECT name FROM groups WHERE id = %s", (c[4],))
                g_name = cur.fetchone()
                data.append({
                    "name": c[1], "email": c[2], "birthday": str(c[3]),
                    "group": g_name[0] if g_name else None, "phones": phones
                })

    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "contacts.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Done. Saved to: {file_path}")

def import_from_json():
    filename = input("File name (default: contacts.json): ") or "contacts.json"
    if not os.path.isabs(filename):
        folder = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(folder, filename)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        with get_connection() as conn:
            with conn.cursor() as cur:
                for item in data:
                    cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
                    exists = cur.fetchone()
                    if exists:
                        action = input(f"Contact '{item['name']}' exists. Overwrite? (y/n): ").lower()
                        if action != 'y': continue
                        cur.execute("DELETE FROM contacts WHERE id = %s", (exists[0],))
                    
                    cur.execute(
                        "INSERT INTO contacts (name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                        (item['name'], item.get('email'), item.get('birthday'))
                    )
                    c_id = cur.fetchone()[0]
                    for p in item.get('phones', []):
                        cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                    (c_id, p['phone'], p['type']))
            conn.commit()
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

def import_from_csv():
    filename = input("CSV File name (default: contacts.csv): ") or "contacts.csv"
    if not os.path.isabs(filename):
        folder = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(folder, filename)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        cur.execute("SELECT id FROM contacts WHERE name = %s", (row['name'],))
                        exists = cur.fetchone()
                        if exists:
                            action = input(f"Contact '{row['name']}' exists. Overwrite? (y/n): ").lower()
                            if action != 'y': continue
                            cur.execute("DELETE FROM contacts WHERE id = %s", (exists[0],))

                        group_name = row.get('group', 'Other')
                        cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (group_name,))
                        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                        g_id = cur.fetchone()[0]

                        birthday = row.get('birthday') if row.get('birthday') != '' else None
                        
                        cur.execute(
                            "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                            (row['name'], row.get('email'), birthday, g_id)
                        )
                        c_id = cur.fetchone()[0]

                        if row.get('phone'):
                            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                        (c_id, row['phone'], row.get('phone_type', 'mobile')))
                conn.commit()
        print("CSV Success")
    except Exception as e:
        print(f"Error: {e}")

def interactive_nav():
    print("Sort by: 1.Name 2.Birthday 3.ID")
    sort_choice = input("> ")
    sort_map = {"1": "name", "2": "birthday", "3": "id"}
    sort_col = sort_map.get(sort_choice, "name")

    limit, offset = 3, 0
    while True:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT name, email FROM contacts ORDER BY {sort_col} LIMIT %s OFFSET %s", (limit, offset))
                rows = cur.fetchall()
                if not rows and offset > 0:
                    offset -= limit
                    continue
                for r in rows:
                    print(f"{r[0]} | {r[1]}")
        cmd = input("[n/p/q]: ").lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        elif cmd == 'q': break

def main():
    while True:
        print("\n1.Search 2.Nav 3.Export 4.ImportJSON 5.AddPhone 6.MoveGroup 7.FilterGroup 8.ImportCSV 0.Exit")
        choice = input("> ")
        if choice == '1': search_extended()
        elif choice == '2': interactive_nav()
        elif choice == '3': export_to_json()
        elif choice == '4': import_from_json()
        elif choice == '5':
            n, p, t = input("Name: "), input("Phone: "), input("Type: ")
            with get_connection() as conn:
                with conn.cursor() as cur: 
                    cur.execute("CALL add_phone(%s,%s,%s)", (n,p,t))
                    conn.commit()
        elif choice == '6':
            n, g = input("Name: "), input("Group: ")
            with get_connection() as conn:
                with conn.cursor() as cur: 
                    cur.execute("CALL move_to_group(%s,%s)", (n,g))
                    conn.commit()
        elif choice == '7': filter_by_group()
        elif choice == '8': import_from_csv()
        elif choice == '0': break

if __name__ == "__main__":
    main()