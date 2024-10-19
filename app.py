from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789qwerty'
menu = [{"name": "Информация", "url": "information"},
        {"name": "Достижения", "url": "achievements"},
        {"name": "Статистика", "url": "statistics"}]


@app.route("/")
def index():
    print(url_for('index')) # аргументом указываем имя функции index
    return render_template('index.html', menu=menu)


@app.route("/achievements", methods=["POST", "GET"])
def achievements():
    if request.method == 'POST':
        if len(request.form["username"]) > 2:
            flash('Достижение добавлено', category='success')
        else:
            flash("Ошибка отправки", category='error')

    print(url_for('achievements'))
    return render_template('achievements.html', title="Достижения", menu=menu)


@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title="Статистика достижений", menu=menu)

# with app.test_request_context():  # искусственное создание запроса, чтобы посмотреть как работает функция
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='selfedu'))


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu), 404


if __name__ == "__main__":
    app.run(debug=True)
