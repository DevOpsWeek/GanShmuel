import datetime, mysql.connector, os, xlrd, json
from flask import Flask, json,request,render_template, redirect ,url_for, send_from_directory,Response
from typing import Sequence
from flask.globals import session

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

bill_port=8083
weight_port=8081
bill_url=f'http://0.0.0.0:{bill_port}'
weight_url=f'http://0.0.0.0:{weight_port}'

@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

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
        book = xlrd.open_workbook(r'in/rates.xlsx')
        sheet = book.sheet_by_name("rates")
        cursor.execute('''DELETE FROM Rates''')
        query = '''REPLACE INTO Rates (product_id, rate, scope)
                VALUES (%s, %s, %s)'''
        for r in range(1, sheet.nrows):
            Product = sheet.cell(r, 0).value
            Rate = sheet.cell(r, 1).value
            Scope = sheet.cell(r, 2).value

            values = (Product, Rate, Scope)
            
            cursor.execute(query, values)
    return render_template("getRates.html")

@app.route('/providers')
def Providers():
    cursor.execute('SElECT provider_name,id FROM Providers')
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
   return redirect(url_for("Providers"))

@app.route('/getID/<name>',methods=['get'])
def getID(name):
   cursor.execute('Select id from Providers where provider_name=%s',(name,))
   results=cursor.fetchall()
   id={"id":results[0][0]}
   return json.dumps(id)


@app.route('/trucks')
def Trucks():
    cursor.execute('select id from Trucks')
    results=cursor.fetchall()
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
        values = values + row
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
   
   
@app.route('/getTruck/<id>')
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
         for i in str(datetime.datetime(x.year,x.month,1)):
             if i.isalnum():
                 t1+=i
        
    if not t2:
        for i in str(x):
            if i.isalnum():
                t2+=i
                
    url=(f'{weight_url}/item/{truck}?from={t1}to&{t2}')
    get=json.load(request.get(url=url))
    return json.dumps(get)

    

   
@app.route('/bill/<id>', methods=["GET"])
def getBill(id):
    x=datetime.datetime.now()
    
    cursor.execute('select provider_name from Providers where id=%s',(id,))
    prov=cursor.fetchall()
    
    t1=request.form.get("from")
    t2=request.form.get("to")
    
    if not prov:
        return Response(status=404)
    if not t1:
        t1=""
        for i in str(datetime.datetime(x.year,x.month,1)):
            if i.isalnum():
               t1 += i
        
    if not t2:
        t2=""
        for i in str(x):
            if i.isalnum():
                t2+=i
                
        
    cursor.execute('select count(*) from Trucks where provider_id=%s',(id,))
    truckCount=cursor.fetchall()
    sessionCount=0
    cursor.execute('select id from Trucks where provider_id=%s',(id,))
    trucks=cursor.fetchall()
    getTrucks_list=[]
    session_ID_list=[]
    
    for id in trucks:
        getTrucks_list.append(json.load(request.get(url=f'{bill_url}/getTruck/{id}?from={t1}to={t2}')))
    
    for dict in getTrucks_list:
       sessionCount += len(dict["session"])
       for i in dict["session"]:
            session_ID_list.append(i)
       
    session_response=[]
    neto_produce_list=[]
    
    for session in session_ID_list:
        session_response.append(json.load(request.get(url=f'{weight_url}/session/{session}')))
        for data in session_response:
          neto_produce_list.append({"neto":data["neto"],"produce":data["produce"]})
    
  
    cursor.execute('select product_id from products')
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
        
    cursor.execute('select product_id,rates,scope from products')
    rates_list=cursor.fetchall()

    total=0
    for dict in products:
      for row in rates_list:
         if row[0] == dict["product"] and row[2] == 'All':
            dict["rates"]=row[1]
            dict["pay"]=dict["rates"] * dict ["amount"]
            total += dict["pay"]
         elif row[0] == dict["product"] and row[2] == prov[0][0]:
              dict["rates"]=row[1]
              dict["pay"]=dict["rates"] * dict ["amount"]
              total += dict["pay"]
            
    
    bill={"id":id,"name":prov[0],"from":t1,"to":t2,"TruckCount":truckCount[0],"SessionCount":sessionCount,"products":products,"total":total}
    return json.dumps(bill)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)