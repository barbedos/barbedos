import time
<<<<<<< Updated upstream
=======
from datetime import datetime
>>>>>>> Stashed changes
from function_apis import get_files, update_file
from torrent_apis import get_torrents, get_torrent_by_id


def main():
    while True:
        active = get_files('in_progress')
        torrents = get_torrents()

        if not active or not torrents:
            return

        for file in active:
            tor = get_torrent_by_id(torrents, file['tor_hash'])
            if not tor:
                print(f'No torrent found for {file}')
                continue

            status = 'in_progress'
            if tor.date_completed:
                status = 'completed'

            update_file(file, {
                'status': status,
                'tor_name': tor.name,
                'tor_size': tor.size,
                'tor_status_message': tor.status_message,
                'tor_progress': tor.percent_progress,
                'tor_date_completed': tor.date_completed
            })
        time.sleep(15)


if __name__ == '__main__':
    main()
