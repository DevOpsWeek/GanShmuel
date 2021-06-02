# import requests
# from flask import jsonify
# from requests.exceptions import HTTPError
# import socket

# from sqlalchemy.testing import fixture
# WEIGHT_PATH = ["/","/health", "/unknown", "/getweight", "/weight", "/session/<id>", "/item/"]

# hostname = socket.gethostname()
# local_ip = socket.gethostbyname(hostname)
# test = f"{'http://'}{local_ip}{':8081'}"
# print("##################")
# print("Local IP:",local_ip,'\n')
# print("Test is running...")
# print("##################")

# for i in WEIGHT_PATH:
#      try:
#          response = requests.get(f"{test}{i}")
#          response.raise_for_status()

#      except HTTPError as http_err:
#          print(f'{"Running to: "}{i}')
#          print(f'HTTP error occurred: {http_err}')


#      except Exception as err:
#          print(f'{"Running to: "}{i}')
#          print(f'{"Server is down. Connection refused."}')


#      else:
#           response = requests.get(f"{test}{i}")
#           print(f'{"Running to: "}{i}')
#           print(f'{"HTTP Successful: response code:"}{response.status_code}')
#      print('\n')



# @fixture:
#     @demo.route('/batch-weight')
#     def auth():
#         json_data = requests.get_json()
#         attribute = json_data[
#     {"id":"T-14409","weight":528,"unit":"lbs"},
#     {"id":"T-16474","weight":682,"unit":"lbs"},
#     {"id":"T-14964","weight":543,"unit":"lbs"},
#     {"id":"T-17194","weight":543,"unit":"lbs"},
#     {"id":"T-17250","weight":563,"unit":"lbs"},
#     {"id":"T-14045","weight":563,"unit":"lbs"},
#     {"id":"T-14263","weight":561,"unit":"lbs"},
#     {"id":"T-17164","weight":631,"unit":"lbs"},
#     {"id":"T-16810","weight":653,"unit":"lbs"},
#     {"id":"T-17077","weight":550,"unit":"lbs"},
#     {"id":"T-13972","weight":629,"unit":"lbs"},
#     {"id":"T-13982","weight":583,"unit":"lbs"},
#     {"id":"T-15689","weight":675,"unit":"lbs"},
#     {"id":"T-14664","weight":541,"unit":"lbs"},
#     {"id":"T-14623","weight":609,"unit":"lbs"},
#     {"id":"T-14873","weight":528,"unit":"lbs"},
#     {"id":"T-14064","weight":539,"unit":"lbs"},
#     {"id":"T-13799","weight":532,"unit":"lbs"},
#     {"id":"T-15861","weight":629,"unit":"lbs"},
#     {"id":"T-16584","weight":633,"unit":"lbs"},
#     {"id":"T-17267","weight":539,"unit":"lbs"},
#     {"id":"T-16617","weight":567,"unit":"lbs"},
#     {"id":"T-16270","weight":587,"unit":"lbs"},
#     {"id":"T-14969","weight":666,"unit":"lbs"},
#     {"id":"T-15521","weight":558,"unit":"lbs"},
#     {"id":"T-16556","weight":558,"unit":"lbs"},
#     {"id":"T-17744","weight":536,"unit":"lbs"},
#     {"id":"T-17412","weight":646,"unit":"lbs"},
#     {"id":"T-15733","weight":651,"unit":"lbs"},
#     {"id":"T-14091","weight":534,"unit":"lbs"},
#     {"id":"T-14129","weight":611,"unit":"lbs"}
#     ]
#     #return jsonify(resp=generate_response(attribute))
print(200)
return 200
