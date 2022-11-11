import psycopg2
from psycopg2 import Error
import logging

logging.basicConfig(level=logging.INFO,
                    filename='logger_for_check_satnums.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Satnums_logger')
with open("base_config.txt", "r") as f:
    text = f.read()

def connect_with_db(text=text):
    connection = psycopg2.connect(text)
    cursor = connection.cursor()

    return connection, cursor

# ТРЕТИЙ ВАРИАНТ, КОГДА НЕТ ПАРАМЕТРОВ ОРБИТЫ НО ЕСТЬ ТОЛЬКО СТРАНА
# запрос на получение таблицы по стране
def create_query_ctry(country, cursor):
    if country is not None:
        select_Query_ctry = f'''select "CTRY" from itu8country where "CTRY_NAME" = '{country}' '''
        cursor.execute(select_Query_ctry)
        ctry = cursor.fetchall()[0][0]
        print(ctry)
        return ctry


# тут ищем номер и название спутника
def create_query_ntc_date(ctry, cursor):
    if ctry is not None:
        select_Query_abbr = f'''select "NTC_ID", "D_RCV" from itu8notice where "ADM0"='{ctry}' '''
        cursor.execute(select_Query_abbr)
        ntc_date = cursor.fetchall()
        return ntc_date


# тут ищем номер и название спутника
def create_query_satnum_satname(ntc, cursor):
    if ntc is not None and str(ntc).isdigit():
        select_Query_satname = f'''select "SAT_NAME", "ID" from itu8sats where "NTC_ID" = {ntc}'''
        cursor.execute(select_Query_satname)
        satname_satnum = cursor.fetchall()
        if len(satname_satnum) > 0:
            return satname_satnum[0]
        else:
            satname_satnum = ['-', '-']
            return satname_satnum
    else:
        satname_satnum = ['-', '-']
        return satname_satnum


# вытаскиваем параметры орбиты по по номеру спутника
def create_query_params(satnum, cursor):
    if satnum is not None and satnum != '-':
        select_Query_satname = f'''select "APOG", "PERIG", "INCLIN_ANG" from itu8orbit where "SATNUM" = {satnum}'''
        cursor.execute(select_Query_satname)
        probe = cursor.fetchall()
        if len(probe) == 0:
            apog, perig, inclin = '-', '-', '-'
        else:
            apog, perig, inclin = probe[0]
        return apog, perig, inclin
    else:
        apog, perig, inclin = '-', '-', '-'
        return apog, perig, inclin


def create_with_only_country(country=None):
    logger.info(f'Ищем данные для страны {country}')
    try:

        connection, cursor = connect_with_db()

        list_for_return = [['SATNUM'], ['APOG'], ['PERIG'], ['INCLIN_ANG'], ['SAT_NAME'], ['COUNTRY'], ['DATE_RCV']]

        # достаем аббревиатуру по которым дальше будем искать части в таблицу
        ctry = create_query_ctry(country, cursor)
        ntc_date = create_query_ntc_date(ctry, cursor)

        for i in ntc_date:
            # достаем страну по аббревиатуре
            list_for_return[5].append(country)
            list_for_return[6].append(i[1])
            satname_satnum = create_query_satnum_satname(i[0], cursor)
            list_for_return[4].append(satname_satnum[0])
            list_for_return[0].append(satname_satnum[1])
            apog, perig, inclin = create_query_params(satname_satnum[1], cursor)
            list_for_return[1].append(apog)
            list_for_return[2].append(perig)
            list_for_return[3].append(inclin)

        if len(list_for_return[0]) > 1:
            logger.info(f'Данные найдены и выведены в интерфейс')
        else:
            logger.info(f'Ничего не найдено =(')

        return list_for_return

    except (Exception, Error) as error:
        logger.info("Ошибка при работе с PostgreSQL", error)
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()


