from typing import List, Dict
from flask import Flask
import mysql.connector
import json

app = Flask(__name__)


def favorite_colors() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'billdb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Trucks')
    results = [{id: provider_id} for (id, provider_id) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    return json.dumps({'trucks': favorite_colors()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')