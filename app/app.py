from typing import List, Dict
from flask import Flask,request,render_template, flash, redirect ,url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
import mysql.connector
import json
from openpyxl import Workbook, load_workbook
import os
from openpyxl.worksheet import worksheet

UPLOAD_FOLDER = './in/'
ALLOWED_EXTENSIONS = {'xlsx'}
UPLOAD_DIRECTORY = "./in/"


app = Flask(__name__)
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/')


	# GET /health	
	# POST /provider	
	# POST /rates	
	# GET /rates	
	# POST /truck	
	# PUT /truck	
	# GET /bill	

#wb = load_workbook(XL_PATH)

#cnx=mysql.connector.connect(user='root',password='root',host='db',port='3306',database='billdb')

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

@app.route('/rates', methods=['GET'])
def getRate():
    return render_template("getRates.html")

@app.route('/downloadrates')
def downloadRates():
    p = "./in/rates.xlsx"
    return send_file(p,as_attachment=True)    

@app.route('/rates', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files["file"]
        file.save(os.path.join(UPLOAD_DIRECTORY, file.filename))
        return render_template("getRates.html", message="success")
    return render_template("getRates.html", message = "Upload")
    

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