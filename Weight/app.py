from flask import Flask, jsonify, render_template, request, redirect, Response
from datetime import datetime
from flaskext.mysql import MySQL
import pandas
import os



app = Flask(__name__)

app.config['MYSQL_PORT'] = '3306'

# run "sudo docker inspect mysql_cont" to find your host address for testing (Boris showed me)
# the second bit increments by 1 every time you run docker compse
# (for example: 172.14.0.2 will become 172.15.0.2 next time you compose) -V. Churikov
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0000'
app.config['MYSQL_DATABASE_DB'] = 'weight'
mysql = MySQL(app)
mysql.init_app(app)

now = datetime.now()  # current date and time
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")



@app.route("/", methods=["GET"])
def index4():
    global conn
    global cursor
    conn = mysql.connect()
    cursor = conn.cursor()
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    try:
        cursor.execute("SELECT 1")
        return Response(status=200)
        #return '<h1>Status Code: 200.</h1>'
    except:
        return Response(status=500)
        #return '<h1>Status Code: 500.</h1>'


# Declaration of function that imports CSV tables into our database
def parse(filePath):
    col_names = ['container_id', 'weight', 'unit']
    tempfilePath = os.path.join(os.getcwd() + '/temp-deleteme.csv') #converted csv copy for processing, will be deleted after
    if filePath.endswith('.json'):
        print("Parsing from current directory: " + os.getcwd()) #debug print
        print("Expected file path:" + filePath) #debug print
        print("")
        jsonData = pandas.read_json(filePath) ####### json not yet functional. breaks on this line -V. Churikov
        jsonData.to_csv(tempfilePath)
        filePath = tempfilePath
    elif not filePath.endswith('.csv'):
        print("ERROR: Failed to parse file, *.csv or *.json file required")
        return "ERROR: Failed to parse file, *.csv or *.json file required"

    csvData = pandas.read_csv(filePath,names=col_names, skiprows=1,)
    csvData.fillna(0, inplace=True)
    print(csvData)
    with open(filePath) as file:
        contents = file.read()
        search_word = 'kg'
        search_word2 = 'lbs'
        if search_word in str.lower(contents):
            print("Reading CSV in kg unit mode...")
        elif search_word2 in str.lower(contents):
            print("Reading CSV In lbs unit mode...")
        else:
            print("ERROR: Weight unit not detected in file (must be kg or lbs)")
            return "error: weight unit not detected in file (must be kg or lbs)"

        for i,row in csvData.iterrows():
            sql = "REPLACE INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
            if search_word in str.lower(contents):
                value = (row['container_id'], row['weight'], "kg")
            elif search_word2 in str.lower(contents):
                value = (row['container_id'],row['weight'], "lbs")

            #print("Executing insert sql query with var sql as:\n", sql, "\nAnd var value as:\n", value)
            cursor.execute(sql, value)
        print("CSV file data inserted successfully!")
        conn.commit()
        if os.path.exists(tempfilePath):
            os.remove(tempfilePath)

@app.route("/db", methods=["GET"]) #SHOWS DATABASE
def index():
    cursor.execute('SELECT * FROM containers_registered')
    datacontainers = cursor.fetchall()
    cursor.execute('SELECT * FROM transactions')
    datatransactions = cursor.fetchall()
    return render_template("db.html", data1=datacontainers, data2=datatransactions)


@app.route("/batch-weight", methods=["POST","GET"])
def index2():
    if request.method == 'POST':
        print(request.files)
        if 'csvfile' not in request.files and 'jsonfile' not in request.files:
            return "Error(1): no file selected. Please go back and select a file to upload."
        if 'csvfile' in request.files:
            file = request.files['csvfile']
        else:
            file = request.files['jsonfile']
        print("USING FILE:", file) #debug
        if file.filename == '':
            return "Error (2): no file selected. Please go back and select a file to upload."
        if file == file: #testing, maybe remove
            newfile = os.path.join('./Samples/', file.filename)
            file.save(newfile)
            print("Parsing ", newfile) #debug
            parse(newfile)
            return redirect("/db")
    return render_template("batch-weight.html")


@app.route("/index.html", methods=["POST", "GET"])
def index3():
    return render_template("index.html")

@app.route("/unknown", methods=["POST", "GET"])
def index5():
    cursor.execute('SELECT * FROM containers_registered WHERE weight=0')
    data = cursor.fetchall()
    return render_template("unknown.html", data=data)

@app.route("/weight", methods=["POST", "GET"])
def weight_ftf():
    rqfm = request.form
    direction = rqfm.get('dir')
    truck_id = rqfm.get('truck')
    containers = rqfm.get('containers')
    bruto = rqfm.get('weight')
    unit = rqfm.get('unit')
    produce = rqfm.get('produce')
    tare = rqfm.get('tare')
    neto = rqfm.get('neto')
    force = rqfm.get('ifmale')
    if containers is not None:
        contarr = containers.split(',')
        brutoarr = bruto.split(',')
        truckTararr = tare.split(',')
        netoarr = neto.split(',')
        print(contarr)
        x=0
        try:
            cursor.execute(
            'SELECT DISTINCT datetime FROM transactions IN (SELECT MAX(datetime) FROM transactions WHERE truck = %s)',
            truck_id)
            lasttime = cursor.fetchall()
            cursor.execute('SELECT DISTINCT direction FROM transactions WHERE truck = %s AND datetime = %s', (truck_id, lasttime))
            lastdir = cursor.fetchall()
            if direction == lastdir and direction != 'none':
                if force == False:
                    return "Truck direction can't be set to the same direction as last time when not in force mode, use force to overwrite"
                else:
                    cursor.execute('DELETE * FROM transactions WHERE truck = %s AND datetime = %s', (truck_id, lasttime))
            elif direction == 'out' and lastdir != 'in':
                return "Truck direction can't be set to 'out' without having previously been set to 'in'"
            elif direction == 'none' and lastdir == 'in':
                return "Truck direction can't be set to 'none' after having previously been set to 'in'"
            else:
                cursor.execute('DELETE * FROM transactions WHERE ')
        except:
            pass

        while x < len(contarr):
            if unit == 'lbs':
                #kg to lbs ratio is 1:2.2 not 1:2, fix tomorrow (Jun 1 2021)
                #known issues: If user inputs lbs into weight.html the value is still sent to transactions table as kg, fix tomorrow
                #known issues: weight.html uploads to database only the first item from user input, fix tomorrow
                #brutoarr[x] /= 2
                pass
            if direction == 'out':
                cursor.execute('INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(datetime.now(), direction, truck_id, contarr[x], brutoarr[x], truckTararr[x], netoarr[x], produce))
                cursor.execute('INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)', (contarr[x], brutoarr[x], unit))
                return redirect("/db")
            else:
                cursor.execute(
                    'INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce) VALUES (%s, %s, %s, %s, %s, %s)',
                    (datetime.now(), direction, truck_id, contarr[x], brutoarr[x], produce))
                cursor.execute('INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)',
                               (contarr[x], brutoarr[x], unit))
                return redirect("/db")

            x += 1
    #don't forget to fill the form before submitting - V. Churikov
    print(direction,truck_id,containers,bruto,unit,produce,tare,neto,force)
    return render_template("weight.html")

@app.route("/session", methods=["POST", "GET"])
def index7():
    return render_template("session.html")

@app.route("/item", methods=["POST", "GET"])
def index8():
    return render_template("item.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

