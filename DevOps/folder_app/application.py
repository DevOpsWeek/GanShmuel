import json,os,subprocess,smtplib
from flask import Flask, request

app = Flask(__name__)
email_dic={"sender":"devweek.ci.mails@gmail.com","rec_billing":["david45453@gmail.com","12345angela54@gmail.com"],\
            "rec_weight":["koren.shoshan@gmail.com","12345angela54@gmail.com"],"rec_devops":"12345angela54@gmail.com","password":"A159753a!"}
         
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_dic['sender'],email_dic['password'])

def send_email(branch_name,sender,reciver,result,comitter):
    massage=f"Hey ! Im the CI server \n\
        i noticed a new push to {branch_name} branch whice was comitted by {comitter}\n\
        the result of the push are : \n{result}"
    server.sendmail(sender,reciver,massage)

def create_docker_compose(command_list,branch_name):
    for i in command_list:
        os.system(i)
    print(f"------- worked on branch {branch_name} -------")
    return True

def run_docker(branch_name):
    os.system("git clone https://github.com/DevOpsWeek/GanShmuel.git")
    command_list=["docker-compose down",f"git checkout --track origin/{branch_name}","docker-compose up -d"]
    if branch_name=="DevOps" or branch_name=="Weight" or branch_name=="Billing":
        os.chdir(f"GanShmuel/{branch_name}")
        run_result=create_docker_compose(command_list,branch_name)  
        if run_result==True:
            print("exucuted the docker compose file ! ")
            return "exucuted the docker compose file ! "
        else:
            print("couldnt run your docker-cmpose file ------------- ABORT  -----------")
            return "couldnt run your docker-cmpose file ------------- ABORT  -----------"
    else:
        print("DIDNT GET ANY BRANCH NAME ! ------------- ABORT  -----------")
        return "DIDNT GET ANY BRANCH NAME ! ------------- ABORT  -----------"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str=request.json
    current_branch=list(json_str['ref'].split("/"))
    commiter=json_str['pusher']['name']
    print(current_branch[2])
    respone=run_docker(current_branch[2])
    try:
        if current_branch[2]=="Weight":
            rec_mail=email_dic['rec_weight']
        elif current_branch[2]=="Billing":
            rec_mail=email_dic['rec_billing']
        elif current_branch[2]=="DevOps":
            rec_mail=email_dic['rec_devops'] 
        send_email(current_branch[2],email_dic['sender'],rec_mail,respone,commiter)
        print("sent email-worked !")
    except:
        print("DIDNT sent email-DIDNT worked !")
    return respone

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)

