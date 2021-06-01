import requests
import socket

##pip install -U requests
##pip install -U pytest pytest-html
##pip install -U jsonschema

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print("Hello,This is a script to test the Billing API")
print(local_ip)

test = f"{'http://'}{local_ip}{':5000/'}"

print(test)

response = requests.get(test)
if response.status_code == 200:
     print("/rates: successfull <",response.status_code,">")
elif response.status_code == 404:
     print('/rates: Failed <404> ')