from typing import List, Dict
from flask import Flask,request,render_template, flash, redirect ,url_for, send_from_directory, send_file,Response
from werkzeug.utils import secure_filename
import mysql.connector
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


@app.route('/providers')
def Providers():
    cursor.execute('SElECT * FROM Providers')
    results = cursor.fetchall()
    return render_template("providers.html",provid_list=results)
    check = cnx.is_connected()
    if check is False:
     return "500"
    return "200"

@app.route('/rates', methods=['GET'])
def getRate():
    return render_template("getRates.html")

@app.route('/downloadrates')
def downloadRates():
    p = "in/rates.xlsx"
    if os.path.exists(os.path.dirname('./app/in/rates.xlsx')):
        return send_file(p,as_attachment=True)
    else:
        return render_template("getRates.html", message = "file not found")
    
@app.route('/rates', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files["file"]
        file.save(os.path.join(os.path.dirname('./app/in/'), file.filename))
        return render_template("getRates.html", message="success")
    return render_template("getRates.html", message = "Upload")
    

@app.route("/postTruck", methods=['POST'])
def getTrucks():
    pass

# @app.route("/putTruck", methods=["PUT"])
# def putTruck():
#     return "truck"

@app.route('/updateProvider',methods=['POST'])
def postProvider():
    prov_name=request.form.get("new_name")
    id=request.form.get("id")
    sql='''UPDATE Providers SET provider_name = %s WHERE id = %s'''
    val=(prov_name,id)
    cursor.execute(sql,val)
    cnx.commit()
    return redirect(url_for("Providers"))

@app.route('/addProvider',methods=['POST'])
def addProvider():
   prov_name=request.form.get("prov_name")
   id=request.form.get("id")
   sql='''INSERT INTO Providers(id,provider_name) VALUES (%s,%s)'''
   val =(id ,prov_name)
   cursor.execute(sql,val)
   cnx.commit()
   return redirect(url_for("Providers"))

@app.route('/trucks')
def Trucks():
    cursor.execute('SElECT * FROM Trucks')
    results = cursor.fetchall()
    return render_template("trucks.html",truck_list=results)



@app.route('/updateTrucks' ,methods=['post'])
def updateTruck():
    truckid=request.form.get("id")
    provid=request.form.get("new_prov_id")
    sql='''UPDATE Trucks SET provider_id = %s WHERE id = %s'''
    val=(provid,truckid)
    cursor.execute(sql,val)
    cnx.commit()
    return redirect(url_for("Trucks"))


@app.route('/addTrucks', methods=['POST'])
def addTruck():
   truckid=request.form.get("id")
   provid=request.form.get("prov_id")
   sql='''INSERT INTO Trucks(id,provider_id) VALUES (%s,%s)'''
   val =(truckid,provid)
   cursor.execute(sql,val)
   cnx.commit()
   return redirect(url_for("Trucks"))
   
@app.route('/bill', methods=["GET"])
def getBill():
   return render_template('bill.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)