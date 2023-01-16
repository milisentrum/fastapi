from fastapi import FastAPI
from models import *
from main_ import *

database: List[People] = [People(id="376df671-46ca-4b78-8676-ee060643bcf8",
                                 last_name="Belkona",gender="female",value=103,label=0)]

# вставка данных в "сервер"
def postDB(ppl: People):
    database.append(ppl)
    return database
with con:
    data = con.execute("SELECT * FROM customers")
    for row in data:
        postDB(People(id=row[0], last_name=row[1], gender=row[2], value=row[3], label=row[4]))

#
#  как-то по-умному сделать добавление названий после '/' в url в другом проекте

app = FastAPI()
mainurl = '/api/database'

#декоратор
# @app.get('/')
# def root():
#      return {'message': 'HI!'}

# : печатать каждую строку бд с новой строки
@app.get(mainurl)
def getDB():
    return database
# сортировка по имени, т.к. по value они уже отсортированы, а по id  нет значения сортировать т.к. оно uuid


# : мб реализовать возможность сортировки по выбранным полям
@app.get(mainurl+'/sort')
async def sortdb():
    return sorted(getDB(), key=lambda people: people[1])

@app.delete(mainurl)
async def deleteItem(ppl:Dict):
    for item in database:
        index = database.index(item)
        for key in ppl:
            # if(database[index][key]==ppl[key]):
            if(item[key]==ppl[key]):
                database.pop(index)
                print('first')
    return database

# : печатать только те данные, что были добавлены
@app.post(mainurl)
async def getdata(ppl: People):
    database.append(ppl)
    return database