from flask import Flask, jsonify, render_template, request
from datetime import datetime
from flaskext.mysql import MySQL
import pandas
import os


app = Flask(__name__)

app.config['MYSQL_PORT'] = '3306'

# run "sudo docker inspect mysql_cont" to find your host address for testing (Boris showed me)
# the second bit increments by 1 every time you run docker compose
# (for example: 172.14.0.2 will become 172.15.0.2 next time you compose) -V. Churikov
app.config['MYSQL_DATABASE_HOST'] = '172.21.0.2'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0000'
app.config['MYSQL_DATABASE_DB'] = 'weight'
mysql = MySQL(app)
mysql.init_app(app)

now = datetime.now()  # current date and time
date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

conn = mysql.connect()
cursor = conn.cursor()

# Declaration of function that imports CSV tables into our database,
# uncomment the function call below this declaration for testing  -V. Churikov
def parse(filePath):
    col_names = ['container_id', 'weight', 'unit']
    tempfilePath = os.path.join(os.getcwd() + '/temp-deleteme.csv') #converted csv copy for processing, will be deleted after
    if filePath.endswith('.json'):
        print("Parsing from current directory: " + os.getcwd()) #debug print
        print("Expected file path:" + filePath) #debug print
        jsonData = pandas.read_json(filePath) ####### json not yet functional. breaks on this line -V. Churikov
        jsonData.to_csv(tempfilePath)
        filePath = tempfilePath
    elif not filePath.endswith('.csv'):
        print("ERROR: Failed to parse file, *.csv or *.json file required")
        return "ERROR: Failed to parse file, *.csv or *.json file required"

    csvData = pandas.read_csv(filePath,names=col_names, skiprows=1)
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

# We will call this function from a front-end interface to import CSV tables into our database -V. Churikov
#parse(os.path.join(os.getcwd() + '/Samples/containers2.csv'))

@app.route("/item/<id>?from=t1&to=t2", methods=["GET"])
def index():
    cursor.execute('''select * from containers_registered''')
    return jsonify(cursor.fetchall())
    #return "This time is: " + date_time -- displays the time


@app.route("/batch-weight.html", methods=["POST","GET"])
def index2():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Error(1): no file selected. Please go back and select a file to upload."
        file = request.files['file']
        print("USING FILE:", file) #debug
        if file.filename == '':
            return "Error (2): no file selected. Please go back and select a file to upload."
        if file == file: #testing, maybe remove
            newfile = os.path.join('./Samples/', request.files['file'].filename)
            file.save(newfile)
            print("Parsing ", newfile) #debug
            parse(newfile)
    return render_template("batch-weight.html")

@app.route("/index.html", methods=["POST","GET"])
def index3():
    return render_template("index.html")
@app.route("/", methods=["GET"])
def index4():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    try:
        cursor.execute("SELECT 1")
        return '<h1>Status Code: 200.</h1>'
    except:
        return '<h1>Status Code: 500.</h1>'


if __name__ == "__main__":
    app.run(debug=True)

