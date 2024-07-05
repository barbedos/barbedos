from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.

THRESHOLD = 3600     # 3600 * 1 hours = 3600
TOR_ACTV_PATH = '/home/brian/torrents/torrent_files/active'
TOR_STAG_PATH = '/home/brian/torrents/torrent_files/staging'
TOR_DONE_PATH = '/home/brian/torrents/torrent_files/done'
ACTV_FILES = '/home/brian/torrents/active/**'
DONE_FILES = '/home/brian/torrents/done/**'

FILECOUNT = 0


def send_email(uptime, contents):
    """Send a predefined email"""

    toaddr = 'barbituate@gmail.com'
    fraddr = 'barbituate@gmail.com'

    msg = MIMEText('Uptime = %f\n\n%d Left\n\n%s' % (uptime, FILECOUNT, contents))
    msg['Subject'] = 'Pimpbox is still up'
    msg['From'] = fraddr
    msg['To'] = toaddr

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('localhost')
    server.sendmail(fraddr, [toaddr], msg.as_string())
    server.quit()

def get_files(path):
    global FILECOUNT
    string = ''
    for f in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
         string += f'{f}\n'
         FILECOUNT += 1
    return string

def get_remaining(path):
    string = ''
    all_files = glob.glob(path, recursive=True)
    files_only = [f for f in all_files if os.path.isfile(f)]
    for file in files_only:
        string += f'{file}\n'
    return string

def get_body():
    body = "Active Torrents:\n----------------\n"
    body += get_files(TOR_ACTV_PATH)
    body += "\nStaged Torrents:\n----------------\n"
    body += get_files(TOR_STAG_PATH)
    body += "\nDone Torrents:\n--------------\n"
    body += get_files(TOR_DONE_PATH)
    body += "\nRemaining Active Files:\n--------------\n"
    body += get_remaining(ACTV_FILES)
    body += "\nRemaining Staged Files:\n--------------\n"
    body += get_remaining(DONE_FILES)

    return body


def main():
    with open('/proc/uptime', 'r') as upfile:
        uptime_seconds = int(float(upfile.readline().split()[0]))

    if uptime_seconds > THRESHOLD:
        # Every hour, send an email
        body = get_body()
        send_email(uptime_seconds, body)

if __name__ == "__main__":
    main()
