import requests
import json

main_url = 'http://127.0.0.1:5000'
endpoint = {
    'home': '/',
    'health': '/health',
    'classify': '/classify'
}

# GET
r = requests.get(main_url + endpoint['health'])

# POST
request_data = {
    'sl': 7.0,
    'sw': 3.3,
    'pl': 1.4,
    'pw': 0.7
}

data1 = {
    'sl': 7.0,
    'sw': 3.3,
    'pl': 1.4,
    'pw': 0.7
}
data2 = {
    'sl': 7.0,
    'sw': 3.2,
    'pl': 4.7,
    'pw': 1.4
}
array_of_data = [data1, data2]
# r = requests.get(main_url + endpoint['classify'])
# r = requests.post(main_url + endpoint['classify'], data=json.dumps({'foo':'bar'}) )
r = requests.post(main_url + endpoint['classify'], json=request_data )

print(r.text)
