import json
import requests
from utorrentapi import UTorrentAPI


FILES = '/files'
BASE = 'https://us-central1-serverless-d2414.cloudfunctions.net'
UTS = 'http://104.155.173.173:8080/gui'
USER = 'barbituate'
PASS = '4PMt%18zBTjyUE#to!P%51d$'


def get_files():
    url = BASE + FILES + '?status=pending'
    res = requests.get(url)
    return res.json()


def add_torrent(utor, file):
    link = file.get('link')
    utor.add_url(link)


def main():
    files = get_files()
    if not files:
        return

    utor = UTorrentAPI(UTS, USER, PASS)
    for file in files:
        add_torrent(utor, file)


if __name__ == '__main__':
    main()
