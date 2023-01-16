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
                        value INT, 
                        label INT); """) #label - значения номера очереди после машинной обработки
            # подготавливаем множественный запрос
            sql = 'INSERT INTO customers (id, last_name, gender, value, label) values(?, ?, ?, ?, ?)'
            # указываем данные для запроса
            data = []
            for x in range(cstmrs_cnt):
                data.append([str(uuid4()), random.choice(list(open("surnames.txt"))).rstrip('\n'),
                             random.choice(['male', 'female']), x, 0])

            # добавляем с помощью множественного запроса все данные сразу
            with con:
                con.executemany(sql, data)


# print content of db
with con:
    data = con.execute("SELECT * FROM customers")
    for row in data:
        print(row)