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


# ПЕРВЫЙ ВАРИАНТ, КОГДА ЕСТЬ ХОТЬ 1 ПАРАМЕТР ОРБИТЫ

# собираем запрос по вытаскиванию параметров орбиты и номера аппарата из таблички ORBIT
def create_query(apog=None, perig=None, inclin=None,
                 delapog=50, delperig=50, delinclin=10):
    if apog is not None or perig is not None or inclin is not None:
        select_Query_orbit = f'''select "SATNUM", "APOG", "PERIG", "INCLIN_ANG" from public.itu8orbit where'''
        if apog is not None:
            select_Query_orbit += f''' "APOG" between {apog - delapog} and {apog + delapog}'''
            if perig is not None or inclin is not None:
                select_Query_orbit += f''' and'''
        if perig is not None:
            select_Query_orbit += f''' "PERIG" between {perig - delperig} and {perig + delperig}'''
            if inclin is not None:
                select_Query_orbit += f''' and'''
        if inclin is not None:
            select_Query_orbit += f''' "INCLIN_ANG" between {inclin - delinclin} and {inclin + delinclin}'''
        return select_Query_orbit
    else:
        return


# тут ищем номер нтс и название спутника
def create_query_satname(satnum, cursor):
    if satnum is not None:
        select_Query_satname = f'''select "SAT_NAME", "NTC_ID" from itu8sats where "ID" = {satnum}'''
        cursor.execute(select_Query_satname)
        name_ntc_date = cursor.fetchall()[0]
        return name_ntc_date
    else:
        return None


# тут мы ищем название страны через поиск аббревиатуры, аббревиатуру ищем по нтс номеру
def create_query_country(ntc, date1, date2, cursor):
    if ntc is not None:
        if date1 is not None and date2 is not None:
            select_Query_abbr = f'''select "ADM0", "D_RCV" from itu8notice where "NTC_ID" = {ntc} and "D_RCV" between
             '{date1}' and '{date2}' '''
        else:
            select_Query_abbr = f'''select "ADM0", "D_RCV" from itu8notice where "NTC_ID" = {ntc} '''
        cursor.execute(select_Query_abbr)
        list_for_ctry_and_date = cursor.fetchall()
        if len(list_for_ctry_and_date) > 0:
            ctry_abbr, date = list_for_ctry_and_date[0]
            select_Query_ctry = f'''select "CTRY_NAME" from itu8country where "CTRY" = '{ctry_abbr}' '''
            cursor.execute(select_Query_ctry)
            ctry = cursor.fetchall()[0][0]
            return ctry, date
        else:
            return None, None
    else:
        return None, None


# собираем список спискорв для первго варианта событий
def create_list_for_table(apog=23600, perig=None, inclin=None,
                          country=None, date_r1=None, date_r2=None,
                          delapog=0, delperig=0, delinclin=0):
    logger.info(f'Ищем данные для апогея = {apog}км, перигея = {perig}км, наклонения = {inclin} градусов')
    try:

        connection, cursor = connect_with_db()

        postgreSQL_select_Query_orbit = create_query(apog=apog, perig=perig, inclin=inclin,
                                                     delapog=delapog, delperig=delperig,
                                                     delinclin=delinclin)
        cursor.execute(postgreSQL_select_Query_orbit)
        # получаем все данные, соответствующие запросу
        orbits = cursor.fetchall()
        # убираем повторы
        orbits = set(orbits)
        j = 0
        # добавляем из одной таблицы столбцы с номером аппарата, апогеем, перегеем и наклонением его же
        list_for_return = [['SATNUM'], ['APOG'], ['PERIG'], ['INCLIN_ANG'], ['SAT_NAME'], ['COUNTRY'], ['DATE_RCV']]
        if country is not None:
            for i in orbits:
                # достаем страну по аббревиатуре
                satnum, apog, perig, inclin = i

                satname, ntc = create_query_satname(satnum, cursor)

                ctry, date = create_query_country(ntc, date_r1, date_r2, cursor)
                if ctry == country and date is not None:
                   list_for_return[0].append(satnum)
                   list_for_return[1].append(apog)
                   list_for_return[2].append(perig)
                   list_for_return[3].append(inclin)
                   list_for_return[4].append(satname)
                   list_for_return[5].append(ctry)
                   list_for_return[6].append(date)
        else:
            for i in orbits:
                # достаем страну по аббревиатуре
                satnum, apog, perig, inclin = i

                satname, ntc = create_query_satname(satnum, cursor)

                ctry, date = create_query_country(ntc, date_r1, date_r2, cursor)

                if ctry is not None and date is not None:
                    list_for_return[0].append(satnum)
                    list_for_return[1].append(apog)
                    list_for_return[2].append(perig)
                    list_for_return[3].append(inclin)
                    list_for_return[4].append(satname)
                    list_for_return[5].append(ctry)
                    list_for_return[6].append(date)



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
