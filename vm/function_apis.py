import json
import requests

FILES = '/files'
BASE = 'https://us-central1-serverless-d2414.cloudfunctions.net'
# BASE = 'http://localhost:8080'


def get_files(status):
    url = BASE + FILES + f'?status={status}'
    res = requests.get(url)
    return res.json()


def update_file(file, data):
    data_d = {
        'id': file.get('id'),
        'data': data
    }
    data_s = json.dumps(data_d)
    url = BASE + FILES
    requests.put(url, data=data_s)
    return 'Success'
