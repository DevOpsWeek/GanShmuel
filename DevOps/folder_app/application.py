import json,os,subprocess 
from flask import Flask, request
app = Flask(__name__)

def create_docker_compose(command_list,branch_name):
    for i in command_list:
        if i==f"{branch_name}/folder_app":
            os.chdir(i)
        else:
            os.system(i)
    print(f"------- worked on branch {branch_name} -------")

def run_docker(branch_name):
    branch_lower=branch_name.lower()  
    command_list=["git clone https://github.com/DevOpsWeek/GanShmuel.git","ls",f"docker rm $(docker stop $(docker ps -a -q --filter=\"name={branch_lower}-container\"))",f"git checkout --track origin/{branch_name}",f"{branch_name}/folder_app",f"docker build -t image/{branch_lower} .",f"docker run -d --name {branch_lower}-container image/{branch_lower}"]
    if branch_name=="DevOps" or branch_name=="Weight" or branch_name=="Billing":
        os.chdir("GanShmuel")
        create_docker_compose(command_list,branch_name)
        print("exucuted the docker compose file ! ")
    else:
        print("DIDNT GET ANY BRANCH NAME !")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str=request.json
    current_branch=list(json_str['ref'].split("/"))
    print(current_branch[2])
    run_docker(current_branch[2])
    return "200"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)

