import json,os
from flask import Flask, request
app = Flask(__name__)

def create_docker_compose(command_list,branch_name):
    os.system(command_list[0])
    os.system(command_list[1])
    os.system(command_list[2])
    os.system(command_list[3])
    print(f"------- worked on branch {branch_name}-------------")

def run_docker(branch_name):
    command_list=["git clone https://github.com/DevOpsWeek/GanShmuel.git","cd GanShmuel",f"git checkout --track origin/{branch_name}","docker run -it hello-world"]
    if branch_name=="DevOps":
        create_docker_compose(command_list,branch_name)
        return ("here Devops")
    elif branch_name=="Weight":
        create_docker_compose(command_list,branch_name)
        return("here Weight")
    elif branch_name=="Billing":
        create_docker_compose(command_list,branch_name)
        return("here Billing")
    elif branch_name=='main':
        create_docker_compose(command_list,branch_name)
        return("here main")
    else:
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

