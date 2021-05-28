from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# from sqlalchemy import inspect
# from sqlalchemy.sql import text
# import os

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8088/Weight'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

now = datetime.now()  # current date and time
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")


@app.route("/item/<id>?from=t1&to=t2", methods=["GET"])
def index():
    return "This time is: " + date_time


@app.route("/batch-weight.html", methods=["POST","GET"])
def index2():
    return render_template("batch-weight.html")

@app.route("/index.html", methods=["POST","GET"])
def index3():
    return render_template("index.html")
@app.route("/", methods=["GET"])
def index4():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    try:
        db.engine.execute('SELECT 1')
        return '<h1>Status Code: 200.</h1>'
    except:
        return '<h1>Status Code: 500.</h1>'


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")

