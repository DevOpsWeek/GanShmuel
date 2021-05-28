import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    str1="200"
    return str1

if __name__ == '__main__':
    app.run()
