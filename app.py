from flask import Flask, render_template, request, redirect
import youtube, os, dbConfig
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = dbConfig.DATABASE_ADDRESS
db = SQLAlchemy(app)


import User
from Login import *

if not os.path.exists(dbConfig.DATABASE_PATH):
    db.create_all()

@app.route('/')
def index():
    podcasts = youtube.get()
    if flask_login.current_user.is_anonymous:
        title = 'Главная страница'
    else:
        title = flask_login.current_user.id
    return render_template('podcasts.html', username=title, podcasts=podcasts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    link = None
    result = None
    if flask_login.current_user.is_anonymous:
        title = 'Главная страница'
    else:
        title = flask_login.current_user.id
    if request.method == 'POST' and 'link' in request.form:
        link = request.form['link']
        result = youtube.download(link)
        if result:
            return redirect("/")
        else:
            result = 'Ошибка загрузки. Проверьте ссылку'
    return render_template('add.html',  username=title, error=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_page = render_template(
        'login.html',
        )

    if request.method == 'GET':
        return login_page

    username = request.form['username']
    record = User.query.filter_by(username=username).first()

    if record is None:
        return login_page

    if request.form['password'] == record.password:
        user = Users()
        user.id = username
        flask_login.login_user(user)
        return redirect('/')

    return login_page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template(
            'SignUp.html',
            )
    login = request.form['username']
    password = request.form['password']
    if login and password:
        User.create(User(login, password))
        user = Users()
        user.id = login
        flask_login.login_user(user)
    return redirect('/')
