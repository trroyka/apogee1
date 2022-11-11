import os

from flask import Flask, render_template, send_from_directory, request

root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")
js_directory = os.path.join(template_folder, "js")
css_directory = os.path.join(template_folder, "css")
images_directory = os.path.join(template_folder, "images")

app = Flask(__name__, template_folder=template_folder)

@app.route("/")
def index():
    with open('страны.txt') as f:
        countries = f.read().splitlines()
    return render_template("index.html", countries=countries, country="Выберите страну")


@app.route("/", methods=['GET', 'POST'])
def move_forward():
    with open('страны.txt') as f:
        l = f.read().splitlines()
    apog = ''  # запрос к данным формы
    perig = ''
    inclin = ''
    datetime1 = ''
    datetime2 = ''
    country = ''
    delapog = 0
    delperig = 0
    delinclin = 0
    # считываем данные из формы, если их нет - задаем нулями
    if request.method == 'POST':
        apog = request.form.get('apog')
        delapog = request.form.get('del_apog')
        if apog.isdigit():
            apog = int(apog)
        else:
            apog = None
        if delapog.isdigit():
            delapog = int(delapog)
        else:
            delapog = 0

        perig = request.form.get('perig')
        delperig = request.form.get('del_perig')
        if perig.isdigit():
            perig = int(perig)
        else:
            perig = None
        if delperig.isdigit():
            delperig = int(delperig)
        else:
            delperig = 0

        inclin = request.form.get('inclin')
        delinclin = request.form.get('del_inclin')
        if inclin.isdigit():
            inclin = int(inclin)
        else:
            inclin = None
        if delinclin.isdigit():
            delinclin = int(delinclin)
        else:
            delinclin = 0

        datetime1 = request.form.get('date_r1')
        if datetime1 == '':
            datetime1 = None

        datetime2 = request.form.get('date_r2')
        if datetime2 == '':
            datetime2 = None

        country = request.form.get('country')
        if country == 'Выберите страну':
            country = None

    if apog is not None or perig is not None or inclin is not None:
        from python_scripts.main_query_for_all import create_list_for_table
        list_of_words = create_list_for_table(apog=apog, perig=perig, inclin=inclin,
                                              date_r1=datetime1, date_r2=datetime2, country=country,
                                              delapog=delapog, delperig=delperig, delinclin=delinclin)

    elif apog == perig == inclin is None and datetime1 is not None and datetime2 is not None:
        print('only with dates')
        from python_scripts.query_for_date_and_country import create_with_date_and_country
        list_of_words = create_with_date_and_country(date_r1=datetime1, date_r2=datetime2, country=country)

    elif apog == perig == inclin == datetime1 == datetime2 is None and country is not None:
        print('only CTRY')
        from python_scripts.query_for_only_country import create_with_only_country
        list_of_words = create_with_only_country(country=country)

    else:
        list_of_words = []
    apog = request.form.get('apog')
    delapog = request.form.get('del_apog')
    if apog == None:
        apog = ''

    if delapog == 0:
        delapog = ''

    if perig == None:
        perig = ''

    if delperig == 0:
        delperig = ''

    if inclin == None:
        inclin = ''

    if delinclin == 0:
        delinclin = ''

    if country == None:
        country = 'Выберите страну'

    return render_template('index.html', dict=list_of_words, countries=l,
                           apog=apog, perig=perig, delapog=delapog, delperig=delperig,
                           delinclin=delinclin, inclin=inclin, date_r1=datetime1,
                           date_r2=datetime2, country=country)


@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory(js_directory, path)


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory(css_directory, path)


@app.route("/images/<path:path>")
def send_images(path):
    return send_from_directory(images_directory, path)


if __name__ == "__main__":
    app.run(host ='0.0.0.0')
