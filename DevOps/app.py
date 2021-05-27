import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
    	info=json.dumps(request.json)
        return info
    else:
        return "didnt work"

if __name__ == '__main__':
    app.run()

