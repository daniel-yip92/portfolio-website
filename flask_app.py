
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_calculator import calculate

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
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

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

"""
@app.route('/result/<rslt>')
def calculate_result(rslt):
        return f"<h1>{rslt}</h1>"
"""