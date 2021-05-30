import json,os,subprocess 
from flask import Flask, request
app = Flask(__name__)

def create_docker_compose(command_list,branch_name):
    for i in command_list:
        os.system(i)
    print(f"------- worked on branch {branch_name} -------")

def run_docker(branch_name):
    #command_list=[f"git checkout --track origin/{branch_name}",f"cd {branch_name}","docker compose up ."]
    if branch_name=="DevOps" or branch_name=="Weight" or branch_name=="Billing":
        #create_docker_compose(command_list,branch_name)
        command="ls"
        os.system(command)
        subprocess.call("script.sh") 
        print("exucuted the docker compose file ! ")
        return "exucuted the docker compose file ! "
    else:
        print("DIDNT GET ANY BRANCH NAME !")
        return "DIDNT GET ANY BRANCH NAME !"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str=request.json
    current_branch=list(json_str['ref'].split("/"))
    print(current_branch[2])
    fun_result=run_docker(current_branch[2])
    print(fun_result)
    return fun_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)