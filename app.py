import pymysql
from flask import Flask,render_template, request
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL(app)
mysql.init_app(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_CURSORCLASS'] = 'dictCursor'


#Creating a connection cursorclear
 
#Executing SQL Statements
#cursor.execute(''' CREATE TABLE table_name(field1, field2...) ''')
#cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
#cursor.execute(''' DELETE FROM table_name WHERE condition ''')
 
#Saving the Actions performed on the DB
#mysql.connection.commit()
 
#Closing the cursor
#cursor.close()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/health")
def getHealth():
    return "server health"

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