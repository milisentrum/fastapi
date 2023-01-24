import sqlite3 as sl
import random
from uuid import uuid4
import names

cstmrs_cnt=600

# открываем файл с базой данных
con = sl.connect('cstmrs.db')
# открываем базу
with con:
    # получаем количество таблиц с нужным нам именем
    data = con.execute("select count(*) from sqlite_master where type='table' and name='customers'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            with con:
                con.execute("""
                    CREATE TABLE customers (
                        id str PRIMARY KEY,
                        last_name VARCHAR(30),
                        gender VARCHAR(10),
                        label INT, 
                        age INT); """) #label - значения номера очереди после машинной обработки
            # подготавливаем множественный запрос
            sql = 'INSERT INTO customers (id, last_name, gender, label, age) values(?, ?, ?, ?, ?)'
            # указываем данные для запроса
            data = []
            for x in range(cstmrs_cnt):
                data.append([str(uuid4()), random.choice(list(open("surnames.txt"))).rstrip('\n'),
                             random.choice(['male', 'female']), 0, random.randint(14, 99)])

            # добавляем с помощью множественного запроса все данные сразу
            with con:
                con.executemany(sql, data)

with con:
    data_queues = con.execute("select count(*) from sqlite_master where type='table' and name='queues'")
    for row in data_queues:
        if row[0] == 0:
            with con:
                con.execute("""
                    CREATE TABLE queues (
                        queue_id str PRIMARY KEY,
                        customer_id str,
                        datetime DATETIME,
                        value INT, 
                        is_hurry BOOLEAN); """)

            sql = 'INSERT INTO queues (queue_id, customer_id, datetime, value, is_hurry) values(?, ?, ?, ?, ?)'
            data_queues = []
            for x in range(20):
                data_queues.append([str(uuid4()), str(uuid4()), '2023-01-01', x, random.choice([0, 1])])
            with con:
                con.executemany(sql, data_queues)

# print content of customers table
with con:
    data = con.execute("SELECT * FROM customers")
    # data = con.execute("SELECT * FROM queues")
    for row in data:
        print(row)