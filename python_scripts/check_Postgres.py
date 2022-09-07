import psycopg2
from psycopg2 import Error
import logging

logging.basicConfig(level=logging.INFO,
                    filename='logger_for_check_satnums.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Satnums_logger')


def create_query(apog=None, perig=None, inclin=None):
    if apog is not None or perig is not None or inclin is not None:
        select_Query_orbit = f'''select "SATNUM", "APOG", "PERIG", "INCLIN_ANG" from public.itu8orbit where'''
        if apog is not None:
            select_Query_orbit += f''' "APOG" between {apog - 100} and {apog + 100}'''
            if perig is not None or inclin is not None:
                select_Query_orbit += f''' and'''
        if perig is not None:
            select_Query_orbit += f''' "PERIG" between {perig - 100} and {perig + 100}'''
            if inclin is not None:
                select_Query_orbit += f''' and'''
        if inclin is not None:
            select_Query_orbit += f''' "INCLIN_ANG" between {inclin - 10} and {inclin + 10}'''
        print(select_Query_orbit)
        return select_Query_orbit

def create_query_satmame(satnum=None):
    if satnum is not None:
        select_Query_orbit = f'''select "SAT_NAME", "NTC_ID" from itu8sats where "ID" = {satnum}'''
        return select_Query_orbit

def create_list_for_table(apog=23600, perig=None, inclin=None):
    logger.info(f'Ищем данные для апогея = {apog}км, перигея = {perig}км, наклонения = {inclin} градусов')
    try:
        connection = psycopg2.connect("host=localhost"
                                      " dbname=itu_base_oracle"
                                      " user=postgres "
                                      " password=123456")

        cursor = connection.cursor()

        postgreSQL_select_Query_orbit = create_query(apog=apog, perig=perig, inclin=inclin)
        cursor.execute(postgreSQL_select_Query_orbit)
        orbits = cursor.fetchall()
        names = cursor.description
        list_for_return = [['SAT_NAME']]
        for a in orbits:
            list_for_return[0].append(1)
        print(orbits)
        j = 1
        for i in names:
            list_for_return.append([i.name])
            for a in orbits:
                list_for_return[j].append(a[j-1])
            j += 1

        if len(list_for_return[0]) > 1:
            logger.info(f'Данные найдены и выведены в интерфейс')
        else:
            logger.info(f'Ничего не найдено =(')

        return list_for_return

    except (Exception, Error) as error:
        logger.info("Ошибка при работе с PostgreSQL", error)
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()



connection = psycopg2.connect("host=localhost"
                              " dbname=itu_base_oracle"
                              " user=postgres "
                              " password=123456")

cursor = connection.cursor()

query = create_query_satmame(satnum=8)
print(query)
cursor.execute(query)
print(cursor.fetchall())