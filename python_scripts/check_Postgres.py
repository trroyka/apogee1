import psycopg2
from psycopg2 import Error
import logging

logging.basicConfig(level=logging.INFO,
                    filename='logger_for_check_satnums.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Satnums_logger')


# тут клепаем запрос на вытаскивание необходимых данных по параметрам из формы
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
        return select_Query_orbit


# тут ищем номер нтс и название спутника
def create_query_satmame(satnum, cursor):
    if satnum is not None:
        select_Query_satname = f'''select "SAT_NAME", "NTC_ID" from itu8sats where "ID" = {satnum}'''
        cursor.execute(select_Query_satname)
        name_ntc_date = cursor.fetchall()[0]
        return name_ntc_date


# тут мы ищем название страны через поиск аббревиатуры, аббревиатуру ищем по нтс номеру
def create_query_country(ntc, cursor):
    if ntc is not None:
        select_Query_abbr = f'''select "ADM0", "D_RCV" from itu8notice where "NTC_ID" = {ntc}'''
        cursor.execute(select_Query_abbr)
        ctry_abbr, date = cursor.fetchall()[0]
        print(ctry_abbr)
        select_Query_ctry = f'''select "CTRY_NAME" from itu8country where "CTRY" = '{ctry_abbr}' '''
        cursor.execute(select_Query_ctry)
        ctry = cursor.fetchall()[0][0]
        return ctry, date


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
        list_for_return = []
        print(orbits)
        j = 0
        for i in names:
            list_for_return.append([i.name])
            for a in orbits:
                list_for_return[j].append(a[j])
            j += 1
        list_for_return.append(['SAT_NAME'])
        list_for_return.append(['COUNTRY'])
        list_for_return.append(['DATE_RCV'])

        for val in list_for_return[0][1:]:
            name, ntc = create_query_satmame(val, cursor)
            list_for_return[j].append(name)
            ctry, date = create_query_country(ntc, cursor)
            list_for_return[j+1].append(ctry)
            list_for_return[j+2].append(date)
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

name, ntc = create_query_satmame(22403, cursor)
print(name, ntc)
ctry, date = create_query_country(ntc, cursor)
print(ctry, date)
