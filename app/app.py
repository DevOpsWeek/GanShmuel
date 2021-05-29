from typing import List, Dict
from flask import Flask,request,render_template
import mysql.connector
import json

app = Flask(__name__)


# def trucks() -> List[Dict]:
#     connection = config_db()
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM Trucks')
#     results = [{id: provider_id} for (id, provider_id) in cursor]
#     cursor.close()
#     connection.close()
#     return results


# def providers() -> List[Dict]:
#     connection=config_db()
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM Providers')
#     results = [{id: name} for (id, name) in cursor]
#     cursor.close()
#     connection.close()
#     return results


cnx=mysql.connector.connect(user='root',password='root',host='db',port='3306',database='billdb')

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/health',methods=['GET'])
def getHealth():
    check = cnx.is_connected()
    if check is False:
     return "500"
    return "200"

@app.route('/providers', methods=['GET'])
def postProvider():
   pass

@app.route('/rates')
def getRate():
    pass


@app.route("/getTrucks", methods=["GET"])
def getTrucks() ->List[Dict]:
    cursor=cnx.cursor()
    cursor.execute('Select * from Trucks')
    results = [{id: name} for (id, name) in cursor]
    cursor.close()
    return json.dumps({'trucks':results})


# @app.route("/truck", methods=["PUT"])
# def putTruck():
#     return "truck"

@app.route("/bill", methods=["GET"])
def getBill():
   return render_template('bill.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)