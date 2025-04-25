import psycopg2
import csv

# подключаемся к базе данных
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# функция для создания таблицы, если её нет
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(15) NOT NULL
        )
    """)
    conn.commit()

# функция для добавления или обновления юзера
def insert_or_update_user(username, phone):
    cur.execute("""
        SELECT 1 FROM phonebook WHERE username = %s
    """, (username,))
    if cur.fetchone():
        # если юзер уже есть, обновляем его телефон
        cur.execute("""
            UPDATE phonebook SET phone = %s WHERE username = %s
        """, (phone, username))
    else:
        # если юзера нет, добавляем его
        cur.execute("""
            INSERT INTO phonebook (username, phone) VALUES (%s, %s)
        """, (username, phone))
    conn.commit()

# функция для добавления юзеров из CSV файла
def insert_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # пропускаем заголовок
        for row in reader:
            username, phone = row
            insert_or_update_user(username, phone)  # добавляем или обновляем юзера
    print("данные успешно вставлены из csv файла.")

# функция для поиска юзеров по шаблону
def search_phonebook(pattern):
    cur.execute("""
        SELECT * FROM phonebook
        WHERE username ILIKE %s OR phone ILIKE %s
    """, ('%' + pattern + '%', '%' + pattern + '%'))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# функция для запроса данных с пагинацией (limit и offset)
def get_phonebook_paginated(limit, offset):
    cur.execute("""
        SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s
    """, (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# функция для удаления юзера по имени или телефону
def delete_user(identifier):
    cur.execute("""
        DELETE FROM phonebook WHERE username = %s OR phone = %s
    """, (identifier, identifier))
    conn.commit()

# основная функция для демонстрации работы
if __name__ == "__main__":
   
    create_table()
    insert_from_csv('contacts.csv')

    # ищем юзеров по шаблону
    print("результаты поиска для 'Nura':")
    search_phonebook('Nura')
    
    print("записи из телефонной книги с пагинацией:")
    get_phonebook_paginated(10, 0)

     
    delete_user('87771234567')

    # закрываем курсор и соединение
    cur.close()
    conn.close()
