from datetime import datetime
from typing import List, Dict
from flask import Flask,request,render_template, flash, redirect ,url_for, send_from_directory, send_file,Response,jsonify
from werkzeug.utils import secure_filename
import mysql.connector
from openpyxl import Workbook, load_workbook
import os
from openpyxl.worksheet import worksheet

UPLOAD_FOLDER = './in/'
RATES_FILE = 'rates.xlsx'
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename): #made for the rates POST so that uploaded files must be .xlsx files 
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/')


	# GET /health x
	# POST /provider x
    # PUT /provider/{id} 	x
	# POST /rates	
	# GET /rates	
	# POST /truck x
	# PUT /truck{id} x
    # GET /truck<id>?from=t1&to=t2 ????
	# GET /bill	


cnx=mysql.connector.connect(user='root',password='root',host='db',port='3306',database='billdb')
cursor=cnx.cursor()


@app.route('/',methods=['GET'])
def index():
    return render_template('base.html')

@app.route('/health',methods=['GET'])
def getHealth():
    if cnx.is_connected() is False:
        return Response(status=500)
    return Response(status=200) 

@app.route('/rates', methods=['GET'])
def getRate():
    return render_template("getRates.html")

@app.route('/rates/download', methods=['GET'])
def downloadRates():
    return send_from_directory(UPLOAD_FOLDER, RATES_FILE, as_attachment=True)

@app.route('/rates', methods=['POST'])
def upload_file():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, RATES_FILE))
    return render_template("getRates.html")
    
@app.route('/providers')
def Providers():
    return render_template("providers.html")

@app.route('/updateProvider',methods=['POST'])
def postProvider():
    new_name=request.form.get("new_name")
    old_name=request.form.get("old_name")
    cursor.execute('select provider_name,id from Providers where provider_name=%s',(old_name,))
    values=(new_name,)
    results=cursor.fetchall()
    for row in results:
        values=values + (row[1],)
    cursor.execute('UPDATE Providers SET provider_name = %s WHERE id = %s',values)
    cnx.commit()
    return redirect(url_for("Providers"))

@app.route('/addProvider',methods=['POST'])
def addProvider():
   new_name=request.form.get("new_name")
   cursor.execute('INSERT INTO Providers(provider_name) VALUES (%s)',(new_name,))
   cnx.commit()
   cursor.execute('Select id from Providers where provider_name=%s',(new_name,))
   results=cursor.fetchall()
   return jsonify(results[0])


@app.route('/trucks')
def Trucks():
    cursor.execute('SElECT Trucks.id,provider_name,provider_id FROM Trucks JOIN Providers where Providers.id=Trucks.provider_id')
    results = cursor.fetchall()
    return render_template("trucks.html",truck_list=results)

@app.route('/updateTruck' ,methods=['post'])
def updateTruck():
    id=request.form.get("id")
    prov=request.form.get("new_prov")
    cursor.execute('Select id from Providers where provider_name=%s',(prov,))
    results=cursor.fetchall()
    values=()
    for row in results:
        values = (row[0],)
    values = values + (id,)
    cursor.execute('UPDATE Trucks SET provider_id = %s WHERE id = %s',values)
    cnx.commit()
    return redirect(url_for("Trucks"))


@app.route('/addTruck', methods=['POST'])
def addTruck():
   id=request.form.get("id")
   prov=request.form.get("prov_name")
   values =(id,)
   cursor.execute('Select id from Providers where provider_name=%s',(prov,))
   results=cursor.fetchall()
   if not results:
        cursor.execute('INSERT INTO Providers(provider_name) VALUES (%s)',(prov,))
        cnx.commit()
        cursor.execute('Select id from Providers where provider_name=%s',(prov,))
        results=cursor.fetchall()
   for row in results:
        values=values+(row[0],)
   cursor.execute('INSERT INTO Trucks(id,provider_id) VALUES (%s,%s)',values)
   cnx.commit()
   return redirect(url_for("Trucks"))
   
   
# @app.route('/getTruck',method=['post'])
# def getTruck():
#     id=request.form.get("id")
#     t1=request.form.get("to")
#     t2=request.form.get("from")
    

   
@app.route('/bill', methods=["GET"])
def getBill():
   return render_template('bill.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)