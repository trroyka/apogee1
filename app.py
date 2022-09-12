import os
import string
import random

from flask import Flask, render_template, redirect, send_from_directory, request, url_for

# from python_scripts.check_Postgres import create_list_for_table


root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")
js_directory = os.path.join(template_folder, "js")
css_directory = os.path.join(template_folder, "css")
images_directory = os.path.join(template_folder, "images")

app = Flask(__name__, template_folder=template_folder)

apog = ''
perig = ''
inclin = ''


@app.route("/")
def index():
    with open('страны.txt') as f:
        l = f.read().splitlines()
    return render_template("index.html", apog=apog, perig=perig, inclin=inclin, countries=l)


@app.route("/", methods=['GET', 'POST'])
def move_forward():
    with open('страны.txt') as f:
        l = f.read().splitlines()
    apog = ''  # запрос к данным формы
    perig = ''
    inclin = ''
    datetime1 = ''
    country = ''
    delapog = 0
    delperig = 0
    delinclin = 0
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

        datetime1 = request.form.get('date_r')
        if datetime1 == '':
            datetime1 = None
        country = request.form.get('country')
        if country == 'Выберите страну':
            country = None
        print(country)
    from python_scripts.check_Postgres import create_list_for_table
    list_of_words = create_list_for_table(apog=apog, perig=perig, inclin=inclin,
                                          date_r=datetime1, country=country,
                                          delapog=delapog, delperig=delperig, delinclin=delinclin)


    return render_template('index.html', dict=list_of_words, countries=l,
                           apog=apog, perig=perig, inclin=inclin, date_r=datetime1, country=country)


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
    app.run()
