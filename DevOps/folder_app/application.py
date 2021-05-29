
import json
from flask import Flask, request
app = Flask(__name__)


def run_docker(branch_name):
    if branch_name=="DevOps":
        pass
    elif branch_name=="Weight":
        pass
    elif branch_name=="Billing":
        pass
    elif branch_name=='main':
        pass
    else:
        return "DIDNT GET ANY BRANCH NAME !"


@app.route('/webhook', methods=['POST'])
def webhook():
    json_str=request.json
    current_branch=list(json_str['ref'].split("/"))
    print(current_branch[2])
    fun_result=run_docker(current_branch)
    print(fun_result)
    return fun_result



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)
