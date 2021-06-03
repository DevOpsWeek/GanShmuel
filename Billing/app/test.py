import requests
from requests.exceptions import HTTPError
import socket

BILLING_PATHS = ["/","/health","/rates","/providers","/rates/download","/trucks","/bill"]

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
test = f"{'http://'}{local_ip}{':5000'}"

for i in BILLING_PATHS:
     
     try:
         response = requests.get(f"{test}{i}")
         response.raise_for_status()
     except HTTPError as http_err:
          print("500")
          break 
     except Exception as err:
          print("500")
          break 
     else:
          response = requests.get(f"{test}{i}")
          print("200")
          break
