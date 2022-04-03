from datetime import datetime
import functions_framework
from firebase_admin import firestore


JSON_KEY_PATH = (
    '/Users/barbe/Projects/barbedos/functions/files/'
    'key.serverless-admin.json')


@functions_framework.http
def files(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        if not request_json:
            return 'failed to get request data'
        link = request_json.get('link')
        name = request_json.get('name')
        add_file(link, name)
        return f'Sucessfully received {name} - {link} added'

    if request.method == 'GET':
        doc_list = get_files(request.args)
        return f'{doc_list}'

    return 'Invalid Method'


def add_file(link, name):
    fdb = firestore.Client().from_service_account_json(
        JSON_KEY_PATH)

    now = datetime.utcnow()
    doc_ref = fdb.collection('files').document()
    doc_ref.set({
        'link': link,
        'name': name,
        'status': 'pending',
        'time_added': now,
        'time_updated': now
    })


def get_files(args):
    fdb = firestore.Client().from_service_account_json(
        JSON_KEY_PATH)

    status = args.get('status', 'pending')
    docs = fdb.collection('files').where(
        'status', '==', status).stream()

    doc_list = []
    for doc in docs:
        print(f'{doc.id} -> {doc.to_dict}')
        doc_list.append({
            'id': doc.id,
            'doc': doc.to_dict()
        })
    return doc_list
