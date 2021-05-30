from typing import List, Dict
from flask import Flask,request,render_template
import mysql.connector
import json

app = Flask(__name__)

	# GET /health x
	# POST /provider
    # PUT /provider/{id} 	
	# POST /rates	
	# GET /rates	
	# POST /truck	
	# PUT /truck{id}	
    # GET /truck<id>?from=t1&to=t2
	# GET /bill	

cnx=mysql.connector.connect(user='root',password='root',host='db',port='3306',database='billdb')
cursor=cnx.cursor()

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/health',methods=['GET'])
def getHealth():
    if cnx.is_connected() is False:
     return "500"
    return "200"

# @app.route('/providers',methods=['POST'])
# def postProvider():
#    pass

# @app.route('/providers',methods=['PUT'])
# def putProvider():
#    pass
   
# @app.route('/postRates',methods=['POST'])
# def postRate():
#     pass

# @app.route('/getRates',methods=['GET'])
# def postRate():
#     pass

# @app.route('/postTruck', methods=['POST'])
# def postTrucks():
#     pass

# @app.route('/getTruck', methods=['GET'])
# def getTrucks():
#     pass

# @app.route('/putTruck', methods=['PUT'])
# def getTrucks():
#     pass


@app.route('/bill', methods=["GET"])
def getBill():
   return render_template('bill.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)