from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [{"name": "Информация", "url": "information"},
        {"name": "Достижения", "url": "achievements"},
        {"name": "Статистика", "url": "statistics"}]

@app.route("/")
def index():
    print(url_for('index')) # аргументом указываем имя функции index
    return render_template('index.html', menu=menu)


@app.route("/achievements")
def achievements():
    print(url_for('achievements'))
    return render_template('achievements.html', title="Достижения", menu=menu)


@app.route("/profile/<username>")
def profile(username, path):
    return f"Пользователь: {username}"


@app.route("/statistics", methods=["POST", "GET"])
def statistics():
    if request.method == 'POST':
        print(request.form)
    return render_template('statistics.html', title="Статистика достижений", menu=menu)

# with app.test_request_context():  # искусственное создание запроса, чтобы посмотреть как работает функция
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('profile', username='selfedu'))

if __name__ == "__main__":
    app.run(debug=True)
