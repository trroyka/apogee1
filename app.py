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

name = 'sputnik'
apog = '-'
perig = '-'
inclin = '-'


@app.route("/")
def index():
    with open('страны.txt') as f:
        l = f.read().splitlines()
    return render_template("index.html", name=name, apog=apog, perig=perig, inclin=inclin, countries=l)


@app.route("/", methods=['GET', 'POST'])
def move_forward():
    with open('страны.txt') as f:
        l = f.read().splitlines()
    apog = None  # запрос к данным формы
    perig = None
    inclin = None
    if request.method == 'POST':
        apog = request.form.get('apog')
        if apog.isdigit():
            apog = int(apog)
        else:
            apog = None
        perig = request.form.get('perig')
        if perig.isdigit():
            perig = int(perig)
        else:
            perig = None
        inclin = request.form.get('inclin')
        if inclin.isdigit():
            inclin = int(inclin)
        else:
            inclin = None

        print(apog, perig, inclin)
    from python_scripts.check_Postgres import create_list_for_table
    list_of_words = create_list_for_table(apog=apog, perig=perig, inclin=inclin)

    return render_template('index.html', dict=list_of_words, countries=l,
                           apog=apog, perig=perig, inclin=inclin)


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
