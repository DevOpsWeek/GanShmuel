import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        return request.json
    else:
        return "didnt work"

if __name__ == '__main__':
    app.run()

