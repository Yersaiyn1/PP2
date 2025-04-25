import psycopg2 ##pip install psycopg2-binary esli vidaet oshibku
import csv

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(15) NOT NULL
        )
    """)
    conn.commit()


def insert_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            username, phone = row
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()

    with open('contacts.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, phone])


def update_user(identifier, new_username=None, new_phone=None):
    if new_username:
        cur.execute("UPDATE phonebook SET username = %s WHERE username = %s OR phone = %s",
                    (new_username, identifier, identifier))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s OR phone = %s",
                    (new_phone, identifier, identifier))
    conn.commit()


def query_data(filter_by=None, value=None):
    if filter_by == "username":
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (value,))
    elif filter_by == "phone":
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (value,))
    else:
        cur.execute("SELECT * FROM phonebook")

    rows = cur.fetchall()
    for row in rows:
        print(row)


def delete_user(identifier):
    cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (identifier, identifier))
    conn.commit()


if __name__ == "__main__":
    create_table()
    # insert_from_csv('contacts.csv')
    insert_from_console()  # Run this to add new user data
    # update_user("John", new_phone="1234567890")
    # query_data("username", "John")
    # delete_user("1234567890")

    cur.close()
    conn.close()