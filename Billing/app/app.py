import datetime
from typing import Sequence
from flask import Flask, json,request,render_template, redirect ,url_for, send_from_directory,Response
from flask.globals import session
import mysql.connector
import os
import json

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
    cursor.execute('SElECT provider_name FROM Providers')
    results = (cursor.fetchall())
    return render_template("providers.html",provid_list=results)

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
   id={"id":results[0][0]}
   return json.dumps(id)


@app.route('/trucks')
def Trucks():
    cursor.execute('SElECT id from Trucks')
    results = cursor.fetchall()
    return render_template("trucks.html",truck_list=results)

@app.route('/updateTruck' ,methods=['post'])
def updateTruck():
    values=()
    id=request.form.get("id")
    prov=request.form.get("new_prov")
    cursor.execute('Select id from Providers where provider_name=%s',(prov,))
    results=cursor.fetchall()
    if not results:
        cursor.execute('INSERT INTO Providers(provider_name) VALUES (%s)',(prov,))
        cnx.commit()
        cursor.execute('Select id from Providers where provider_name=%s',(prov,))
        results=cursor.fetchall()
    for row in results:
        values = values + (row[0],id)
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
   
   
@app.route('/getTruck/<id>?from=<t1>&to=<t2>')
def getTruck(id):
    x=datetime.datetime.now()
    cursor.execute('select id from Trucks where id=%s',(id,))
    results=cursor.fetchall()
    truck=results[0][0]
    t1=request.form.get("from")
    t2=request.form.get("to")
    if not results:
        return Response(status=404)
    if not t1:
        t1= str(datetime.datetime(x.year,x.month,1))
    if not t2:
        t2=str(x)
    url=(f'http://0.0.0.0:5001/item/{truck}?from={t1}to&{t2}')
    item=json.load(request.get(url=url))
    get={"id":truck,"from":t1,"to":t2,"tara":item["tara"],"session":item["session"]}
    return json.dumps(get)

    

   
@app.route('/bill/<id>', methods=["GET"])
def getBill(id):
    x=datetime.datetime.now()
    sessionCount=0
    
    cursor.execute('select id,provider_name from Providers where id=%s',(id,))
    prov=cursor.fetchall()
    
    t1=request.form.get("from")
    t2=request.form.get("to")
    
    if not prov:
        return Response(status=404)
    if not t1:
        t1=str(datetime.datetime(x.year,x.month,1))
    if not t2:
        t2=str(x)
        
    cursor.execute('select count(*) from Trucks where provider_id=%s',(id,))
    truckCount=cursor.fetchall()
    
    cursor.execute('select id from Trucks where provider_id=%s',(id,))
    trucks=cursor.fetchall()
    getTrucks_list=[]
    session_ID_list=[]
    for id in trucks:
        ID=id
        getTrucks_list.append(json.load(request.get(url=f'http://0.0.0.0:5000/getTruck/{ID}?from={t1}to={t2}')))
    
    for dict in getTrucks_list:
       sessionCount += len(dict["session"])
       for i in dict["session"]:
            session_ID_list.append(i)
       
    session_response=[]
    neto_produce_list=[]
    for session in session_ID_list:
        session_response.append(json.load(request.get(url=f'http://0.0.0.0:5001/session/{session}')))
        neto_produce_list.append({"neto":session_response["neto"],"produce":session_response["produce"]})
    
  
    cursor.execute('select product_name from products')
    product_name=cursor.fetchall()    
    products=[]
    for name in product_name:
        count=0
        amount=0
        for dict in neto_produce_list:
            if name == dict["produce"]:
                count +=1
                amount += dict["neto"]
        products.append({"product":name,"count":count,"amount":amount})
    
    
    
     
    
    bill={"id":prov[0][0],"name":prov[0][1],"from":t1,"to":t2,"TruckCount":truckCount[0][0]}
    # return json.dumps(bill)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)