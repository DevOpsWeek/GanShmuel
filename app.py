import pymysql
import pymysql.cursors
from flask import Flask,render_template, request
#from flaskext.mysql import MySQL


app = Flask(__name__)
conn = pymysql.connect(host='localhost',
                             user='billdb',
                             password='billdb123',
                             database='billdb',
                             cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/health", methods=['GET'])
def getHealth():
    cur.execute("select 1")
    output = cur.fetchall()
    return output


@app.route("/provider", methods=["POST"])
def postProvider():
    return "provider"


@app.route('/form')
def form():
    return render_template('form.html')

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
    return "bill"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    mysqlconnect()

