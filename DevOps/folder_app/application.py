import json,os,subprocess,smtplib
from flask import Flask, request

# User pools for emails confirmation
email_dic={"sender":"devweek.ci.mails@gmail.com","rec_billing":["david45453@gmail.com","12345angela54@gmail.com"],\
            "rec_weight":["koren.shoshan@gmail.com","12345angela54@gmail.com"],"rec_devops":"12345angela54@gmail.com","password":"A159753a!"}

# Start Email service & Login
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_dic['sender'],email_dic['password'])

# First clone into our git repo and checkout into all our branches
os.system("git clone https://github.com/DevOpsWeek/GanShmuel.git")
os.chdir("GanShmuel")
os.system("git checkout --track origin/Billing")
os.system("git checkout --track origin/Weight")
os.system("git checkout --track origin/DevOps")
os.chdir("DevOps/folder_app")

# Sending mail funcation ( according to the CI results )
def send_email(branch_name,sender,reciver,result,comitter):
    massage=f"Hey ! Im the CI server \n\
        i noticed a new push to {branch_name} branch whice was comitted by {comitter}\n\
        the result of the push are : \n{result}"
    server.sendmail(sender,reciver,massage)
  
# Prod env to run dockoer-compose up for each branch
def create_docker_compose(command_list,branch_name):
    for i in command_list:
        os.system(i)
    if branch_name=="Weight":
         os.environ['WEIGHT_PORT']="8081"
         print(os.environ['WEIGHT_PORT'])
         os.system("docker-compose -p WEIGHT_Stage up -d")
    elif branch_name=="Billing":
         os.environ['BILLING_PORT']="8083"
         print(os.environ['BILLING_PORT'])
         os.system("docker-compose up -p BILLING_Stage -d")
    elif branch_name=="main":
         os.environ['BILLING_PORT']="8084"
         print(os.environ['BILLING_PORT'])
         os.system("docker-compose -p BILLING_PROD up -d")
         os.environ['WEIGHT_PORT']="8082"
         print(os.environ['WEIGHT_PORT'])
         os.system("docker-compose -p WEIGHT_PROD up -d") 
    print(f"------- worked on branch {branch_name} -------")


# Test evn - if succesfull returns 200 (  each branch gets tested with thier provided tests )
def test_env (branch_name):
    if(branch_name=="Billing"):
        os.environ['BILLING_PORT']="8085"
        os.system("git checkout Weight")
        os.chdir("/app/GanShmuel/Weight")
        os.system("docker-compose -p Weight_test up -d")
        os.system("git checkout Billing")
        os.chdir("/app/GanShmuel/Billing/app")
        os.system("docker-compose -p Billing_test up -d")
        os.system("chmod +x test.py")
        result=subprocess.check_output("python3 ./test.py")
        return result
    elif branch_name=="Weight":
        os.environ['WEIGHT_PORT']="8086"
        os.system("git checkout Weight")
        os.chdir("/app/GanShmuel/Weight")
        os.system("docker-compose -p Weight_test up -d")
        os.system("chmod +x test.py")
        result=subprocess.check_output(['python3', './test.py'])
    elif branch_name=="main":
        result=200
    print(result)
    return result

# Main funcation - run tests 
def run_docker(branch_name):
    command_list=[f"git checkout {branch_name}",f"git pull origin {branch_name}","docker-compose down"]      
    if branch_name=="Weight" or branch_name=="Billing" or branch_name=="main":
        os.chdir(f"/app/GanShmuel/{branch_name}")
        test_result=test_env(branch_name)
        if test_result==200:
            create_docker_compose(command_list,branch_name)
            print("exucuted the docker-compose file !!")
            return "exucuted the docker-compose file !!"
        else:
            print("couldnt run your docker-compose file ! --- ABORT ---")
            return "couldnt run your docker-compose file ! --- ABORT ---"
    else:
        print("DIDNT GET ANY VALID BRANCH NAME ! --- ABORT ---")
        return "DIDNT GET ANY VALID BRANCH NAME ! --- ABORT ---"


app = Flask(__name__)
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
    app.run(host='0.0.0.0', port=8080,  debug=True , use_reloader=False)


