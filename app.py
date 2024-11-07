# Вкарване на нужните библиотеки! 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
from random import randint

app = Flask(__name__, static_url_path='/static')

# Къде ще се запазва информацията за базата данни
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Създаване на object на SQLAlchemy
db = SQLAlchemy(app)

@app.before_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))
    custom = db.Column("custom", db.String())

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url():
    letters  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    size = request.form["urlSize"]
    customAlias = request.form["customAlias"]
    print(letters)
    # Проверка, ако URL адреса вече съществува
    while True:
        if size:
            rand_letters = random.choices(letters, k=size)
            return
        rand_letters = random.choices(letters, k=7)
        rand_letters = "".join(rand_letters)
        if customAlias:
            short_url = Urls.query.filter_by(custom=customAlias).first()
        else:
            short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            if customAlias:
                return customAlias
            else:
                return rand_letters


# Back-end за началната страница
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["longUrl"]
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
       
        return render_template('index.html')

# Back-end за страницата на генерирания URL адрес
@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template('notfound.html')

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

if __name__ == '__main__':
    app.run(debug=True)