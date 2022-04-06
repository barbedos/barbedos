import json
import requests
from utorrentapi import UTorrentAPI


FILES = '/files'
BASE = 'https://us-central1-serverless-d2414.cloudfunctions.net'
# BASE = 'http://localhost:8080'
UTS = 'http://104.155.173.173:8080/gui'
USER = 'barbituate'
PASS = '4PMt%18zBTjyUE#to!P%51d$'


def get_files():
    url = BASE + FILES + '?status=pending'
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


def add_torrent(utsvr, file):
    link = file.get('link')
    utsvr.add_url(link)


def main():
    files = get_files()
    if not files:
        return

    utsvr = UTorrentAPI(UTS, USER, PASS)
    for file in files:
        add_torrent(utsvr, file)
        update_file(file, {'status': 'in_progress'})


if __name__ == '__main__':
    main()
