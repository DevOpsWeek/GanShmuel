import os
from datetime import datetime, date, time

import numpy
import pandas
from flask import Flask, jsonify, render_template, request, redirect, Response, url_for
from flaskext.mysql import MySQL



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


def listmatx(arr, arg):
    list_1 = []
    for i in range(arr.shape[0]):
        j = 0
        for a in arg.split(','):
            list_1.append((a + ':' + str(arr[int(i)][int(j)])))
            j += 1
    return list_1


def tuple_dict(t, l):
    new_dic = dict()
    for i, j in enumerate(l):
        new_dic[j] = t[i]
    return new_dic


@app.route("/", methods=["GET"])
def index4():
    global conn
    global cursor
    conn = mysql.connect()
    cursor = conn.cursor()
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1")
        return Response(status=200)
        # return '<h1>Status Code: 200.</h1>'
    except:
        return Response(status=500)
        # return '<h1>Status Code: 500.</h1>'


# Declaration of function that imports CSV tables into our database
def parse(filePath):
    col_names = ['container_id', 'weight', 'unit']
    tempfilePath = os.path.join(
        os.getcwd() + '/temp-deleteme.csv')  # converted csv copy for processing, will be deleted after
    if filePath.endswith('.json'):
        print("Parsing from current directory: " + os.getcwd())  # debug print
        print("Expected file path:" + filePath)  # debug print
        print("")
        jsonData = pandas.read_json(filePath)  ####### json not yet functional. breaks on this line -V. Churikov
        jsonData.to_csv(tempfilePath)
        filePath = tempfilePath
    elif not filePath.endswith('.csv'):
        print("ERROR: Failed to parse file, *.csv or *.json file required")
        return "ERROR: Failed to parse file, *.csv or *.json file required"

    csvData = pandas.read_csv(filePath, names=col_names, skiprows=1, )
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

        for i, row in csvData.iterrows():
            sql = "REPLACE INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
            if search_word in str.lower(contents):
                value = (row['container_id'], row['weight'], "kg")
            elif search_word2 in str.lower(contents):
                value = (row['container_id'], row['weight'], "lbs")

            # print("Executing insert sql query with var sql as:\n", sql, "\nAnd var value as:\n", value)
            cursor.execute(sql, value)
        print("CSV file data inserted successfully!")
        conn.commit()
        if os.path.exists(tempfilePath):
            os.remove(tempfilePath)


@app.route("/db", methods=["GET"])  # SHOWS DATABASE
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM containers_registered')
    datacontainers = cursor.fetchall()
    cursor.execute('SELECT * FROM transactions')
    datatransactions = cursor.fetchall()
    cursor.execute('SELECT * FROM sessions')
    datasessions = cursor.fetchall()
    return render_template("db.html", data1=datacontainers, data2=datatransactions, data3=datasessions)


@app.route("/cleardb", methods=["GET"])  # SHOWS DATABASE
def cleardb():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions')
    cursor.execute('DELETE FROM containers_registered')
    cursor.execute('DELETE FROM sessions')
    return render_template("db.html")


@app.route("/batch-weight", methods=["POST", "GET"])
def index2():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        print(request.files)
        if 'csvfile' not in request.files and 'jsonfile' not in request.files:
            return "Error(1): no file selected. Please go back and select a file to upload."
        if 'csvfile' in request.files:
            file = request.files['csvfile']
        else:
            file = request.files['jsonfile']
        print("USING FILE:", file)  # debug
        if file.filename == '':
            return "Error (2): no file selected. Please go back and select a file to upload."
        if file == file:  # testing, maybe remove
            newfile = os.path.join('./Samples/', file.filename)
            file.save(newfile)
            print("Parsing ", newfile)  # debug
            parse(newfile)
            return redirect("/db")
    return render_template("batch-weight.html")


@app.route("/index.html", methods=["POST", "GET"])
def index3():
    return render_template("index.html")

@app.route("/unknown", methods=["GET"])
def index5():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM containers_registered WHERE weight=0')
    data = cursor.fetchall()
    if data:
        Response(status=200)
    else:
        Response(status=500)
    return render_template("unknown.html", data=data)



@app.route("/getweight", methods=["GET", "POST"])
def getweight():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == "POST":
        t1 = request.form.get('t1')
        t2 = request.form.get('t2')
        f3 = request.form.get('f')
        #session = request.form.get('ses')
        if t1 == '':
            t1 = datetime.combine(date.today(), datetime.min.time())
        if t2 == '':
            t2 = datetime.today().replace(day=1)
        if f3 == '':
            f3 = 'in,out,none'
        return redirect((url_for('getweight', t1=t1, t2=t2, f=f3)))
    rqfm = request.form
    t1 = rqfm.get('from')
    t2 = rqfm.get('to')
    f3 = rqfm.get('f')
    #session = rqfm.get('ses')
    if t1 == '':
        t1 = datetime.combine(date.today(), datetime.min.time())
    if t2 == '':
        t2 = datetime.now()
    args = request.args
    if 't1' in args and 't2' and 'f' in args:
        fromqs = args.get('t1')
        toqs = args.get('t2')
        myfilter = args.get('f')
        myfilter = myfilter.split(',')
        #session = args.get('ses')
        #print(session)
        if len(myfilter) == 1:
            cursor.execute(
                'SELECT sessions.session_id, transactions.direction, transactions.bruto, transactions.neto, transactions.produce, transactions.containers FROM transactions, sessions WHERE ((sessions.datetime > %s AND sessions.datetime < %s) AND transactions.direction = %s)',
                (fromqs, toqs, myfilter[0]))
        elif len(myfilter) == 2:
            cursor.execute(
                'SELECT sessions.session_id, transactions.direction, transactions.bruto, transactions.neto, transactions.produce, transactions.containers FROM transactions, sessions WHERE ((sessions.datetime > %s AND sessions.datetime < %s) AND transactions.direction = %s OR transactions.direction = %s)',
                (fromqs, toqs, myfilter[0], myfilter[1]))
        elif len(myfilter) >= 3:
            cursor.execute(
                'SELECT sessions.session_id, transactions.direction, transactions.bruto, transactions.neto, transactions.produce, transactions.containers FROM transactions, sessions WHERE ((sessions.datetime > %s AND sessions.datetime < %s) AND transactions.direction = %s OR transactions.direction = %s OR transactions.direction = %s)',
                (fromqs, toqs, myfilter[0], myfilter[1], myfilter[2]))
        else:
            cursor.execute(
                'SELECT sessions.session_id, transactions.direction, transactions.bruto, transactions.neto, transactions.produce, transactions.containers FROM transactions, sessions WHERE sessions.datetime > %s AND sessions.datetime < %s',
                (fromqs, toqs))
        return jsonify(cursor.fetchall())
    return render_template('getweight.html')


@app.route("/weight", methods=["GET", "POST"])
def weight_ftf():
    conn = mysql.connect()
    cursor = conn.cursor()
    rqfm = request.form
    direction = rqfm.get('dir')
    truck_id = rqfm.get('truck')
    containers = rqfm.get('containers')
    bruto = rqfm.get('weight')
    unit = rqfm.get('unit')
    produce = rqfm.get('produce')
    tare = rqfm.get('tare')
    neto = rqfm.get('neto')
    force = rqfm.get('gender')
    if containers is not None:
        contarr = containers.split(',')
        brutoarr = bruto.split(',')
        brutoarrlbtokg = bruto.split(',')
        truckTararr = tare.split(',')
        netoarr = neto.split(',')
        print(contarr)
        x = 0
        try:
            cursor.execute('SELECT MAX(datetime) FROM transactions WHERE truck = %s GROUP BY truck', truck_id)
            lasttime = cursor.fetchall()
            lasttime = str(lasttime).split('(')
            lasttime = str(lasttime).split(',')
            lasttime = str(lasttime).replace('\"', '')
            lasttime = str(lasttime).replace('\'', '')
            lasttime = str(lasttime).replace(" ", "")
            lasttime = str(lasttime).split(',')
            lasttime = str(lasttime[3]) + '-' + str(lasttime[4]) + '-' + str(lasttime[5]) + ' ' + str(
                lasttime[6]) + ':' + str(lasttime[7]) + ':' + str(lasttime[8])
            lasttime = str(lasttime).replace(')', '')
            lasttime = datetime.strptime(str(lasttime), '%Y-%m-%d %H:%M:%S')
            cursor.execute('SELECT DISTINCT direction FROM transactions WHERE truck = %s AND datetime = %s',
                           (truck_id, lasttime))
            lastdir = cursor.fetchall()
            if 'in' in str(lastdir):
                lastdir = 'in'
            elif 'out' in str(lastdir):
                lastdir = 'out'
            elif 'none' in str(lastdir):
                lastdir = 'none'
            if direction == lastdir and direction != 'none':
                print(str(force))
                if str(force) == 'male':
                    return "Truck direction can't be set to the same direction as last time when not in force mode, use force to overwrite"
                else:
                    cursor.execute('DELETE FROM transactions WHERE truck = %s AND datetime = %s', (truck_id, lasttime))
                    conn.commit()
                    cursor.execute('DELETE FROM containers_registered WHERE container_id = %s', contarr[x])
                    conn.commit()
            elif direction == 'out' and lastdir != 'in':
                return "Truck direction can't be set to 'out' without having previously been set to 'in'"
            elif direction == 'none' and lastdir == 'in':
                return "Truck direction can't be set to 'none' after having previously been set to 'in'"
        except:
            pass
        while x < len(contarr):
            if unit == 'lbs':
                brutoarrlbtokg[x] = int(float(brutoarr[x]) / 2.2)
            if direction == 'out':
                cursor.execute('UPDATE sessions SET datetime = %s WHERE truck = %s', (datetime.now(), truck_id))
                conn.commit()
                try:
                    cursor.execute('DELETE FROM transactions WHERE truck = %s AND datetime = %s', (truck_id, lasttime))
                    conn.commit()
                except:
                    pass
                try:
                    cursor.execute('DELETE FROM containers_registered WHERE container_id = %s', contarr[x])
                    conn.commit()
                except:
                    pass
                cursor.execute(
                    'INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (datetime.now(), direction, truck_id, contarr[x], brutoarrlbtokg[x], truckTararr[x], netoarr[x],
                     produce))
                cursor.execute('INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)',
                               (contarr[x], brutoarr[x], unit))
                conn.commit()
            else:
                try:
                    cursor.execute('DELETE FROM transactions WHERE truck = %s AND datetime = %s', (truck_id, lasttime))
                    conn.commit()
                except:
                    pass
                try:
                    cursor.execute('DELETE FROM containers_registered WHERE container_id = %s', contarr[x])
                    conn.commit()
                except:
                    pass
                cursor.execute(
                    'INSERT INTO transactions (datetime, direction, truck, containers, bruto, produce) VALUES (%s, %s, %s, %s, %s, %s)',
                    (datetime.now(), direction, truck_id, contarr[x], brutoarrlbtokg[x], produce))
                conn.commit()
                cursor.execute('INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)',
                               (contarr[x], brutoarr[x], unit))
                conn.commit()
                if x == 0:
                    cursor.execute('INSERT INTO sessions (truck, datetime) VALUES (%s, %s)', (truck_id, datetime.now()))
                    conn.commit()
            x = x + 1

    # don't forget to fill the form before submitting - V. Churikov
    print(direction, truck_id, containers, bruto, unit, produce, tare, neto, force)
    conn.commit()
    return render_template("weight.html")

def item_bug(to):
    to = to.replace("]", '')
    to = to.replace("[", '')
    to = to.replace("\\", '')
    to = to.replace("'", '')
    to = to.replace('"', '')
    to = to.replace(")", '')
    to = to.replace("(", '')
    to = to.replace(",", '')
    return to


@app.route("/item/<id>", methods=["GET", "POST"])
def get_item(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    print(id)
    to = request.args.get('to')
    print(to)
    fr = request.args.get('from')
    print(fr)

    if not to:
        # cursor.execute("SELECT DATE_FORMAT(NOW(), '%Y-%m-%d-%h-%m-%s')")
        # to = cursor.fetchall()
        # to = str(list(to))
        # to = item_bug(to)
        to = datetime.now()
    if not fr:
        # cursor.execute("SELECT DATE_FORMAT(NOW() ,'%Y-%m-01-00-00')")
        # fr = cursor.fetchall()
        # fr = str(list(fr))
        # fr = item_bug(fr)
        fr = datetime.today().replace(day=1)
    cursor.execute("SELECT DISTINCT IFNULL(transactions.truckTara, 'na' ), transactions.id, sessions.session_id"
                   " FROM transactions JOIN sessions ON transactions.truck=sessions.truck"
                   " WHERE (transactions.id='{}') AND (sessions.datetime BETWEEN '{}' AND '{}');".format(id, fr, to))
    ans = cursor.fetchall()

    if not ans:
        cursor.execute("SELECT IFNULL(transactions.truckTara, 'na' ), container_id , session_id "
                       "FROM containers_registered JOIN transactions ON "
                       "containers_registered.container_id=transactions.containers "
                       "JOIN sessions ON sessions.truck=transactions.truck "
                       "WHERE (container_id='{}') AND (sessions.datetime BETWEEN '{}' AND '{}');".format(id, fr, to))
        ans = cursor.fetchall()

    if not ans:
        return Response(status=404)

    res = tuple_dict(ans[0], ("tara", "id", "session"))
    return jsonify(res)


@app.route("/session/<id>", methods=["POST", "GET"])
def index7(id):
    if id == '0':
        return "/session/<id> is up and running!"
    requrl = request.url
    requrl = requrl.split('/')
    requrl = requrl[(len(requrl) - 1)]
    sesid = requrl
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT DISTINCT transactions.direction FROM transactions, sessions WHERE transactions.truck = sessions.truck AND sessions.session_id = %s',
        sesid)
    directions = str(cursor.fetchall())
    if 'in' in directions:
        directions = 'in'
    elif 'out' in directions:
        directions = 'out'
    elif 'none' in directions:
        directions = 'none'
    print(directions)
    if directions == "out":
        query = "SELECT transactions.id, sessions.truck, transactions.bruto, transactions.neto, transactions.truckTara, transactions.produce FROM transactions join sessions on transactions.truck = sessions.truck WHERE (sessions.session_id='{}')".format(
            id)
        cursor.execute(query)
        return jsonify(cursor.fetchall())
        conn.commit()
        res = cursor.fetchall()
        cursor.close()
        args = numpy.array(res)
        return jsonify(listmatx(args, 'id,truck,bruto,neto,truckTara'))
    if directions == 'in' or directions == 'none':
        query = "SELECT transactions.id, sessions.truck, transactions.bruto, transactions.neto, transactions.truckTara, transactions.produce FROM transactions join sessions on transactions.truck = sessions.truck WHERE (sessions.session_id='{}')".format(id)
        # query = "SELECT transactions.id , transactions.bruto , sessions.truck FROM transactions join sessions on transactions.truck =sessions.truck WHERE (sessions.session_id='{}')".format(id)
        cursor.execute(query)
        return jsonify(cursor.fetchall())
        conn.commit()
        res = cursor.fetchall()
        cursor.close()
        args = numpy.array(res)
        return jsonify(listmatx(args, 'id,truck,bruto,neto,truckTara'))
    # return render_template("session.html")
    return jsonify(directions)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
