import time
from function_apis import get_files, update_file
from torrent_apis import add_torrent, get_active_torrents


def get_new_torrent(active_files, torrents):
    # Find the torrent that's not already in database
    tors = sorted(torrents, key=lambda x: x.date_added, reverse=True)
    for tor in tors:
        match_found = False
        for file in active_files:
            if file.get('hash') and file.get('hash') == tor.hash:
                print('torrent hash already in use')
                match_found = True
                break
        if match_found:
            continue
        return tor
    return None


def main():
    pending = get_files('pending')
    if not pending:
        return

    for file in pending:
        active = get_files('in_progress')
        add_torrent(file)
        torrents = get_active_torrents()
        while True:
            tor = get_new_torrent(active, torrents)
            if tor:
                break
            print('New torrent not found yet')
            time.sleep(5)

        update_file(file, {
            'status': 'in_progress',
            'tor_hash': tor.hash,
            'tor_name': tor.name,
            'tor_size': tor.size,
            'tor_status_message': tor.status_message,
            'tor_progress': tor.percent_progress,
            'tor_date_added': tor.date_added
        })


if __name__ == '__main__':
    main()
