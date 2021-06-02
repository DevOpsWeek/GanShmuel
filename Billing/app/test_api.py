import requests
from requests.exceptions import HTTPError
import socket

BILLING_PATHS = ["/","/health","/rates","/providers","/rates/download","/trucks","/bill"]

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
test = f"{'http://'}{local_ip}{':5000'}"
print("##################")
print("Local IP:",local_ip,'\n')
print("Test is running...")
print("##################")

for i in BILLING_PATHS:
     try:
         response = requests.get(f"{test}{i}")
         response.raise_for_status()

     except HTTPError as http_err:
         print(f'{"Running to: "}{i}')
         print(f'HTTP error occurred: {http_err}')

     except Exception as err:
         print(f'{"Running to: "}{i}')
         print(f'{"Server is down. Connection refused."}')

     else:
          response = requests.get(f"{test}{i}")
          print(f'{"Running to: "}{i}')
          print(f'{"HTTP Successful: response code:"}{response.status_code}')
     print('\n')