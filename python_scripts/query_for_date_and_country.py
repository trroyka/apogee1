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

# ВТОРОЙ ВАРИАНТ, КОГДА НЕТ ПАРАМЕТРОВ ОРБИТЫ НО ЕСТЬ ДАТА И СТРАНА ИЛИ ТОЛЬКО ДАТЫ
# запрос на получение таблицы по диапазону дат
def create_query_ctry_ntc(date1, date2, cursor):
    if date1 is not None and date2 is not None:
        select_Query_abbr = f'''select "ADM0", "NTC_ID", "D_RCV" from itu8notice where "D_RCV" between '{date1}' and '{date2}' '''
        cursor.execute(select_Query_abbr)
        ctry_abbr_ntc_date = cursor.fetchall()
        return ctry_abbr_ntc_date


# тут ищем номер и название спутника
def create_query_country(ctry_abbr, cursor):
    if ctry_abbr is not None:
        select_Query_ctry = f'''select "CTRY_NAME" from itu8country where "CTRY" = '{ctry_abbr}' '''
        cursor.execute(select_Query_ctry)
        ctry = list(cursor.fetchone())
        return ctry[0]


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


def create_with_date_and_country(date_r1, date_r2, country=None):
    logger.info(f'Ищем данные для диапазона дат:{date_r1} - {date_r2}, страна {country}')
    try:

        connection, cursor = connect_with_db()

        list_for_return = [['SATNUM'], ['APOG'], ['PERIG'], ['INCLIN_ANG'], ['SAT_NAME'], ['COUNTRY'], ['DATE_RCV']]


        # достаем аббревиатуру и нтс по которым дальше будем искать части в таблицу
        ctry = create_query_ctry_ntc(date_r1, date_r2, cursor)
        print(ctry)
        for i in ctry:
            # достаем страну по аббревиатуре
            list_for_return[5].append(create_query_country(i[0], cursor))
            satname_satnum = create_query_satnum_satname(i[1], cursor)
            list_for_return[4].append(satname_satnum[0])
            list_for_return[0].append(satname_satnum[1])
            list_for_return[6].append(i[2])
            apog, perig, inclin = create_query_params(satname_satnum[1], cursor)
            list_for_return[1].append(apog)
            list_for_return[2].append(perig)
            list_for_return[3].append(inclin)
        print("!!!!!!!!!!!!!!!!", country)
        if country is not None:
            for i in range(len(list_for_return[5]) - 1, 0, -1):
                print("!!!!!!!!!!!!!!!!", country)
                print(str(list_for_return[5][i]))
                if str(list_for_return[5][i]) != country:
                    for j in list_for_return:
                        j.pop(i)


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


