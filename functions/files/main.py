from datetime import datetime
import json
import functions_framework
from firebase_admin import firestore


# JSON_KEY_PATH = (
#      '/Users/barbe/Projects/barbedos/key.serverless-admin.json')
# FDB = firestore.Client().from_service_account_json(
#      JSON_KEY_PATH)
FDB = firestore.Client()
PASSWORD = 'server-file-add'


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
        password = request.form.get('fieldp')
        if password != PASSWORD:
            return '', 200

        link = request.form.get('fieldl')
        name = request.form.get('fieldn')
        add_file(link, name)
        return '', 201

    if request.method == 'GET':
        doc_list = get_files(request.args)
        return f'{doc_list}'

    if request.method == 'PUT':
        request_json = json.loads(request.data)
        if not request_json:
            return 'failed to get request data'
        id_ = request_json.get('id')
        data = request_json.get('data')
        update_file(id_, data)
        return 'Success'

    return 'Invalid Method', 400


def add_file(link, name):
    now = datetime.utcnow()
    doc_ref = FDB.collection('files').document()
    doc_ref.set({
        'link': link,
        'name': name,
        'status': 'pending',
        'time_added': now,
        'time_updated': now
    })


def update_file(id_, data):
    doc_ref = FDB.collection('files').document(id_)
    doc_ref.update(data)


def get_files(args):
    status = args.get('status', 'pending')
    docs = FDB.collection('files').where(
        'status', '==', status).stream()

    doc_list = []
    for doc in docs:
        doc_d = doc.to_dict()
        doc_d['id'] = doc.id
        doc_list.append(doc_d)
    return json.dumps(doc_list, sort_keys=True, default=str)
