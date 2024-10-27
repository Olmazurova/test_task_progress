import sqlite3
import os
from flask import Flask, render_template, request, g, url_for, flash, session, redirect, abort
from FDataBase import FDataBase

# конфигурация с помощью глобальных переменных
DATABASE = '/tmp/flsite1.db'
DEBUG = True
SECRET_KEY = 'dsopisd(*/sdl;fk#gsdklgdfk45f4dfg'

app = Flask(__name__)
app.config.from_object(__name__) # в скобках указываем из какого модуля будем загружать конфигурацию

# здесь формируем полный путь к базе данных,
# root_path - выдаёт полный путь к каталогу, в котором находится этот файл
# а дальше указываем имя файла с БД
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite1.db')))


def connect_db():
    '''Общая функция для установления соединения с БД'''

    conn = sqlite3.connect(app.config['DATABASE']) # методу пердаём путь где расположена БД
    conn.row_factory = sqlite3.Row # Чтобы записи из БД были представлены не в виде кортежей, а в виде словаря
    return conn


def create_db():
    '''Вспомогательная функция для создания таблиц БД (без запуска веб-сервера)'''

    db = connect_db() # функция, которую определили выше
    with app.open_resource('sq_db.sql', mode='r') as f: # читаем файл sql-скриптов, которые и будут генерировать таблицы
        db.cursor().executescript(f.read()) # запускаем выполнение скриптов в прочитанном файле

    db.commit() # записываем изменения в БД
    db.close() # закрываем соединение с БД


def get_db():
    '''Соединение с БД, если оно ещё не установлено'''

    if not hasattr(g, 'link_db'): # проверяем есть ли у обекта g свойство link_db, если нет устанавливаем
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.get_menu(), achievs=dbase.get_achiev_anonce())


@app.route("/achievements", methods=["POST", "GET"])
def achievements():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST': # Если данные от формы пришли
        if len(request.form["title"]) > 4 and len(request.form['description']) > 10:
            res = dbase.add_achieve(request.form['title'], request.form['points'], request.form['description'])
            if not res:
                flash("Ошибка добавления достижения", category='error')
            else:
                flash('Достижение добавлено', category='success')
        else:
            flash("Ошибка добавления достижения", category='error')

    return render_template('achievements.html', title="Достижения", menu=dbase.get_menu())


@app.route("/statistics")
def statistics():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('statistics.html', title="Статистика достижений", menu=dbase.get_menu())


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=dbase.get_menu())


@app.route("/achievements/<int:id_achievement>")
def showAchiev(id_achievement):
    db = get_db()
    dbase = FDataBase(db)
    title, text, points = dbase.get_achieve(id_achievement)
    if not title:
        abort(404)

    return render_template('achieve.html', menu=dbase.get_menu(), title=title, text=text, points=points)


@app.errorhandler(404)
def pageNotFount(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('page404.html', title='Страница не найдена', menu=dbase.get_menu()), 404


@app.teardown_appcontext # декоратор срабатывает тогда, когда происходит уничтожение контекста приложения, тогда можно и соединение с БД закрывать
def close_db(error):
    '''Закрвываем соединение с БД, если оно было установлено'''

    if hasattr(g, 'link_db'):
        g.link_db.close()



if __name__ == "__main__":
    app.run(debug=True)
