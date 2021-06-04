import requests
from requests.exceptions import HTTPError
import socket
WEIGHT_PATH = ["/","/health", "/unknown", "/getweight", "/health", "/batch-weight", "/getweight", "/weight", "/item/0", "/session/0"]

successes = 0
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
test = f"{'http://'}{local_ip}{':5000'}"
#print("##################")
#print("Local IP:",local_ip,'\n')
#print("Test is running...")
#print("##################")

for i in WEIGHT_PATH:
     try:
         response = requests.get(f"{test}{i}")
         response.raise_for_status()

     except HTTPError as http_err:
         #print(f'{"Running to: "}{i}')
         #print(f'HTTP error occurred: {http_err}')
         # response(status = 500)
         pass

     except Exception as err:
         #print(f'{"Running to: "}{i}')
         #print(f'{"Server is down. Connection refused."}')
         # response(status=500)
         pass

     else:
        response = requests.get(f"{test}{i}")
        #print(f'{"Running to: "}{i}')
        #print(f'{"HTTP Successful: response code:"}{response.status_code}')
        successes += 1
        #print('\n')

     if successes >= len(WEIGHT_PATH)-1:
        print("200")
        #print("Successfully connected to web service")



