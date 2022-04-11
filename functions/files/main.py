from datetime import datetime
import time
import json
import functions_framework
from firebase_admin import firestore
from google.cloud import compute_v1

VMPROJ = 'mythical-mason-137313'
VMINST = 'pimpbox'
VMZONE = 'us-central1-a'

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
        start_vm()
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
    data['time_updated'] = datetime.utcnow()
    convert_to_date(data, 'tor_date_added')
    convert_to_date(data, 'tor_date_completed')
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


def start_vm():
    op_client = compute_v1.ZoneOperationsClient()
    inst_client = compute_v1.InstancesClient()
    inst = inst_client.get(
        project=VMPROJ, zone=VMZONE, instance=VMINST
    )
    if (inst.status == 'RUNNING'):
        return 'VM already running'

    opr = inst_client.start_unary(
        project=VMPROJ, zone=VMZONE, instance=VMINST
    )
    start = time.time()
    while opr.status != compute_v1.Operation.Status.DONE:
        opr = op_client.wait(operation=opr.name, zone=VMZONE, project=VMPROJ)
        if time.time() - start >= 300:  # 5 minutes
            raise TimeoutError()
    return 'VM Started'


def convert_to_date(data, key):
    if key not in data:
        return
    data[key] = datetime.fromtimestamp(data[key])
