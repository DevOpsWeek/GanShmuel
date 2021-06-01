import requests
import socket

##pip install -U requests
##pip install -U pytest pytest-html
##pip install -U jsonschema

BILLING_PATHS = ["/","/health","/rates","/providers","/rates/download","/updateProvider","/addProvider","/trucks","/updateTrucks","/addTrucks","/bill"]
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
test = f"{'http://'}{local_ip}{':5000'}"

print("Hello,This is a script to test the Billing API")
print("Local ip:",local_ip)

for i in BILLING_PATHS:
     response = requests.get(f"{test}{i}")
     if response.status_code == 200:
          print(f"{i}"": Successful <",response.status_code,">")
     else:
          print(f"{i}"": Failed <",response.status_code,">")