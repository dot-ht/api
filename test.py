import imp
import requests
import json

request = requests.get('localhost:5000/planets/')
print(json.dumps(request.json))