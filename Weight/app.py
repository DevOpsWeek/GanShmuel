from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

now = datetime.now() # current date and time
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
db = SQLAlchemy(app)

@app.route("/", methods=["GET"])
def index():
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