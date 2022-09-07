import psycopg2
from psycopg2 import Error

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect("host=localhost dbname=itu_base_oracle user=postgres password=123456")

    cursor = connection.cursor()
    postgreSQL_select_Query_orbit = "select * from itu8orbit"
    postgreSQL_select_Query_satname = "select * from itu8sats"

    cursor.execute(postgreSQL_select_Query_orbit)
    print("Выбор строк из таблицы mobile с помощью cursor.fetchall")
    orbits = cursor.fetchall()

    cursor.execute(postgreSQL_select_Query_satname)
    print("Выбор строк из таблицы mobile с помощью cursor.fetchall")
    sats = cursor.fetchall()

    apog = int(input("введите значение апогея"))
    perig = int(input("введите значение перигнея"))
    inclin = int(input("введите значение наклонения"))

    for row in orbits:
        if row[9] in range(apog - 50, apog + 50):
            if row[11] in range(perig - 50, perig + 50):
                if row[5] in range(inclin - 10, inclin + 10):
                    print("SATNUM =", row[1])
                    print("APOG =", row[9])
                    print("PERIG =", row[11])
                    print("INCLIN =", row[5])
                    for line in sats:
                        if line[0] == row[1]:
                            print('SATNAME = ', line[2], '\n')







except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
