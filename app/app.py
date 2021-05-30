from typing import List, Dict
from flask import Flask,request,render_template,redirect,url_for,Response
import mysql.connector
import json

app = Flask(__name__)

	# GET /health x
	# POST /provider
    # PUT /provider/{id} 	
	# POST /rates	
	# GET /rates	
	# POST /truck x
	# PUT /truck{id}	
    # GET /truck<id>?from=t1&to=t2
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

# @app.route('/postproviders',methods=['POST'])
# def postProvider():
#    pass

# @app.route('/putproviders',methods=['PUT'])
# def putProvider():
#    pass
   
# @app.route('/postRates',methods=['POST'])
# def postRate():
#     pass

# @app.route('/getRates',methods=['GET'])
# def postRate():
#     pass

@app.route('/addTrucks', methods=['POST'])
def postTrucks():
   truckid=request.form.get("truck_id")
   provid=request.form.get("prov_id")
   val=(truckid,provid)
   post_truck="INSERT into Trucks (id,provider_id) VALUES(%s,%s)"
   cursor.execute(post_truck,val)
   cnx.commit()
   return redirect(url_for("getTrucks"))
   

@app.route('/trucks', methods=['GET'])
def getTrucks():
    cursor.execute('SElECT * FROM Trucks')
    results = cursor.fetchall()
    return render_template("trucks.html",truck_list=results)

@app.route('/updateTrucks/<string:id>')
def putTrucks(id):
    truckid=id
    provid=request.form["new_prov_id"]
    val=(provid,truckid)
    put_trucks="UPDATE Trucks SET provider_id =%s WHERE id=%s"
    cursor.execute(put_trucks,val)
    return 
    
    
    


@app.route('/bill', methods=["GET"])
def getBill():
   return render_template('bill.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)