
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for, json
from flask_sqlalchemy import SQLAlchemy
from flask_calculator import calculate
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="danielyip",
    password="Newpassword1",
    hostname="danielyip.mysql.pythonanywhere-services.com",
    databasename="danielyip$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

@app.route('/', methods=["GET", "POST"])
def index():
    weatherData = ''
    url = "https://api.open-meteo.com/v1/forecast?latitude=1.2897&longitude=103.8501&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability&daily=weathercode&timezone=Asia%2FSingapore"
    if request.method == "GET":
        headers = {'Accept': 'application/json'}
        weatherData = requests.get(url, headers=headers).json()
        data_dict = dict.fromkeys(weatherData.get('hourly').get('time'), [])
        time_key_update = list(data_dict.keys())
        zipped_weather_data = list(zip(weatherData.get('hourly').get('temperature_2m'), weatherData.get('hourly').get('relativehumidity_2m'), weatherData.get('hourly').get('apparent_temperature'), weatherData.get('hourly').get('precipitation_probability')))
        data_dict.update(list(zip(time_key_update, zipped_weather_data)))
        return render_template("main_page.html", comments=Comment.query.all(), data=data_dict)
    else:
        return 'Not json'

    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/calculator/', methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        first_int = request.form.get("inputNumber1", type=int)
        second_int = request.form.get("inputNumber2", type=int)
        operator = request.form.get("operator")
        result = calculate(first_int, second_int, operator)
        #return redirect(url_for("calculate_result", rslt=result))
        return render_template("calculator.html", result=result)
    else:
        return render_template("calculator.html")


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login_page.html', error=False)

    if request.form["username"] != "admin" or request.form["password"] != "secret":
        return render_template("login_page.html", error=True)

    return redirect(url_for('index'))