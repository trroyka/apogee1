import psycopg2
from psycopg2 import Error
import logging

logging.basicConfig(level=logging.INFO,
                    filename='logger_for_check_satnums.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Satnums_logger')


# тут клепаем запрос на вытаскивание необходимых данных по параметрам из формы
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


def create_query_satmame(satnum, cursor):
    if satnum is not None:
        select_Query_satname = f'''select "SAT_NAME", "NTC_ID" from itu8sats where "ID" = {satnum}'''
        cursor.execute(select_Query_satname)
        name_ntc_date = cursor.fetchall()[0]
        return name_ntc_date
    else:
        return None


# тут мы ищем название страны через поиск аббревиатуры, аббревиатуру ищем по нтс номеру
def create_query_country(ntc, cursor):
    if ntc is not None:
        select_Query_abbr = f'''select "ADM0", "D_RCV" from itu8notice where "NTC_ID" = {ntc}'''
        cursor.execute(select_Query_abbr)
        ctry_abbr, date = cursor.fetchall()[0]
        select_Query_ctry = f'''select "CTRY_NAME" from itu8country where "CTRY" = '{ctry_abbr}' '''
        cursor.execute(select_Query_ctry)
        ctry = cursor.fetchall()[0][0]
        return ctry, date
    else:
        return None, None


def create_list_for_table(apog=23600, perig=None, inclin=None,
                          country=None, date_r=None,
                          delapog=0, delperig=0, delinclin=0):
    logger.info(f'Ищем данные для апогея = {apog}км, перигея = {perig}км, наклонения = {inclin} градусов')
    try:
        connection = psycopg2.connect("host=localhost"
                                      " dbname=itu_base_oracle"
                                      " user=postgres "
                                      " password=123456")

        cursor = connection.cursor()

        postgreSQL_select_Query_orbit = create_query(apog=apog, perig=perig, inclin=inclin,
                                                     delapog=delapog, delperig=delperig, delinclin=delinclin)
        cursor.execute(postgreSQL_select_Query_orbit)
        # получаем все данные, соответствующие запросу
        orbits = cursor.fetchall()
        names = cursor.description
        list_for_return = []
        # убираем повторы
        orbits = set(orbits)
        j = 0
        # добавляем из одной таблицы столбцы с номером аппарата, апогеем, перегеем и наклонением его же
        for i in names:
            list_for_return.append([i.name])
            for a in orbits:
                list_for_return[j].append(a[j])
            j += 1
        # обавляем из других таблиц названия, страны и дату получения
        list_for_return.append(['SAT_NAME'])
        list_for_return.append(['COUNTRY'])
        list_for_return.append(['DATE_RCV'])

        for val in list_for_return[0][1:]:
            name, ntc = create_query_satmame(val, cursor)
            list_for_return[j].append(name)
            ctry, date = create_query_country(ntc, cursor)
            list_for_return[j + 1].append(ctry)
            list_for_return[j + 2].append(date)
        # print(date_r)
        # если есть дата - сортируем по ней
        if date_r is not None:
            for i in range(len(list_for_return[6]) - 1, 0, -1):
                if str(list_for_return[6][i]) != date_r:
                    for j in list_for_return:
                        j.pop(i)

        if country is not None:
            for i in range(len(list_for_return[5]) - 1, 0, -1):
                if f'"{str(list_for_return[5][i])}"' != country:
                    for j in list_for_return:
                        j.pop(i)

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
