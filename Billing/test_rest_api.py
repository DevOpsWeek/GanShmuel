import requests

##pip install -U requests
##pip install -U pytest pytest-html
##pip install -U jsonschema

def test_index():
     response = requests.get("http://www.google.com")
     assert response.status_code == 200

def test_rates():
     response = requests.get("http://www.kkkkaplan.com")
     assert response.status_code == 200

def test_providers():
     response = requests.get("http://www.kkkkaplan.com")
     assert response.status_code == 200