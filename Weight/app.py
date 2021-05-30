from flask import Flask, jsonify, render_template, request, redirect, Response
from flask_table import Table, Col
import logging
from datetime import datetime
from flaskext.mysql import MySQL
import pandas
import os


app = Flask(__name__)

app.config['MYSQL_PORT'] = '3306'

# run "sudo docker inspect mysql_cont" to find your host address for testing (Boris showed me)
# the second bit increments by 1 every time you run docker compse
# (for example: 172.14.0.2 will become 172.15.0.2 next time you compose) -V. Churikov
app.config['MYSQL_DATABASE_HOST'] = '172.19.0.2'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0000'
app.config['MYSQL_DATABASE_DB'] = 'weight'
mysql = MySQL(app)
mysql.init_app(app)

now = datetime.now()  # current date and time
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/", methods=["GET"])
def index4():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    try:
        cursor.execute("SELEC 1")
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
    data = cursor.fetchall()
    return render_template("unknown.html", data=data)


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
def index6():
    return render_template("weight.html")

@app.route("/session", methods=["POST", "GET"])
def index7():
    return render_template("session.html")

@app.route("/item", methods=["POST", "GET"])
def index8():
    return render_template("item.html")



if __name__ == "__main__":
    app.run(debug=True)
