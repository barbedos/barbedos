from utorrentapi import UTorrentAPI, TorrentListInfo


UTS = 'http://104.155.173.173:8080/gui'
USER = 'barbituate'
PASS = '4PMt%18zBTjyUE#to!P%51d$'
UTSVR = UTorrentAPI(UTS, USER, PASS)


def add_torrent(file):
    link = file.get('link')
    UTSVR.add_url(link)


def get_torrents():
    data = UTSVR.get_list()
    tor_list = TorrentListInfo(data)
    return tor_list.torrents


def get_active_torrents():
    new_tors = []
    for tor in get_torrents():
        if tor.date_completed or tor.status_message == 'Stopped':
            continue
        new_tors.append(tor)
    return new_tors


def get_torrent_by_id(tors, hash_id):
    for tor in tors:
        if tor.hash == hash_id:
            return tor
    return None
