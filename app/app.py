from typing import List, Dict
from flask import Flask,request,render_template
import mysql.connector
import json

from mysql.connector import connection

app = Flask(__name__)


def conn_db():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'billdb'
    }
    connection = mysql.connector.connect(**config)
    return connection

def trucks() -> List[Dict]:

    connection=conn_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Trucks')
    results = [{id: provider_id} for (id, provider_id) in cursor]
    cursor.close()
    connection.close()
    return results

def health():
    connection = conn_db()
    cursor = connection.cursor()
    cursor.execute('SELECT 1')
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/trucks')
def getTrucks() -> str:
    return json.dumps({'trucks': trucks()})

@app.route('/health')
def getHealth()->str:
    return json.dumps(health())

@app.route("/provider", methods=["POST"])
def postProvider():
    return "provider"


@app.route('/form')
def form():
    return 'imagine this is a form'

@app.route("/rates", methods=["GET", "POST"])
def getPOSTRates():
    if request.method == 'GET':
        return "Showig rates"
    
    if request.method == 'POST':
        product_id = request.form['product_id']
        rate = request.form['rate']
        scope = request.form['scope']
        cursor = mysql.get_db().cursor()
        cursor.execute(''' INSERT INTO rates_table VALUES(%s,%s)''',(product_id,rate,scope))
        mysql.get_db.commit()
        cursor.close()
        return f"Done!!"

@app.route("/truck", methods=["POST"])
def postTruck():
    return "truck"

@app.route("/truck", methods=["PUT"])
def putTruck():
    return "truck"

@app.route("/bill", methods=["GET"])
def getBill():
    return render_template('bill.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')