from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import os

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8088/Weight'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


now = datetime.now() # current date and time
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

@app.route("/", methods=["GET"])
def index():
    #db.engine.execute('mysql -V')
    return "This time is: " + date_time

@app.route("/health", methods=["GET"])
def health():
    try:
        db.engine.execute('SELECT 1')
        return '<h1>Status Code: 200.</h1>'
    except:
        return '<h1>Status Code: 500.</h1>'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8088 ,debug=True)