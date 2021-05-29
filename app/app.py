from typing import List, Dict
from flask import Flask,request,render_template
import mysql.connector
import json

app = Flask(__name__)

	# GET /health	
	# POST /provider	
	# POST /rates	
	# GET /rates	
	# POST /truck	
	# PUT /truck	
	# GET /bill	


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

@app.route('/providers')
def postProvider():
   pass

@app.route('/rates')
def getRate():
    pass


@app.route("/postTruck", methods=['POST'])
def getTrucks():
    pass



# @app.route("/putTruck", methods=["PUT"])
# def putTruck():
#     return "truck"

@app.route("/bill", methods=["GET"])
def getBill():
   return render_template('bill.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)