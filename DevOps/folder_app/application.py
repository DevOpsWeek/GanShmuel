import json,os,subprocess 
from flask import Flask, request
app = Flask(__name__)

def create_docker_compose(command_list,branch_name):
    for i in command_list:
        if i==f"{branch_name}":
            os.chdir(i)
        else:
            os.system(i)
    print(f"------- worked on branch {branch_name} -------")

def run_docker(branch_name):
    branch_lower=branch_name.lower()  
    os.system("git clone https://github.com/DevOpsWeek/GanShmuel.git")
    command_list=["docker-compose down",f"git checkout --track origin/{branch_name}",f"{branch_name}",f"docker build -t image/{branch_lower} .","docker-compose up -d"]
    if branch_name=="DevOps" or branch_name=="Weight" or branch_name=="Billing":
        os.chdir("GanShmuel")
        create_docker_compose(command_list,branch_name)
        print("exucuted the docker compose file ! ")
        return "exucuted the docker compose file ! "
    else:
        print("DIDNT GET ANY BRANCH NAME ! ------------- ABORT  -----------")
        return "DIDNT GET ANY BRANCH NAME ! ------------- ABORT  -----------"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str=request.json
    current_branch=list(json_str['ref'].split("/"))
    print(current_branch[2])
    respone=run_docker(current_branch[2])
    return respone

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)

