import psycopg2
from config import host, login, password, db_name
from create_bot import bot


def sql_start():
    global db_connection, cursor
    db_connection = psycopg2.connect(
        host=host,
        user=login,
        password=password,
        database=db_name
    )
    cursor = db_connection.cursor()
    print("Database connected")
    cursor.execute('CREATE TABLE IF NOT EXISTS materials(id SERIAL primary key, name TEXT, material TEXT, data_type NUMERIC(1))')
    db_connection.commit()


async def add_material(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO materials(name,material,data_type) VALUES(%s,%s,%s)', (data['name'], data['material'], data['data_type']))
        db_connection.commit()


async def get_data():
    cursor.execute('SELECT * FROM materials;')
    return cursor.fetchall()


async def get_data_id(id: int):
    cursor.execute('SELECT material, data_type FROM materials where id = %s;', [id])
    return cursor.fetchall()