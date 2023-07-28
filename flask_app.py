
# Mini Project A and B
# Web App created with Python on the Flask framework, incorporating MySQL db
# Created by Daniel Yip
# July 2023

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_calculator import calculate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
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
mirate = Migrate(app, db)
app.secret_key = "hammerrandomlyonsomekeys5"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

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

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
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
        return render_template("calculator.html", result=result)
    else:
        return render_template("calculator.html")


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login_page.html', error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
