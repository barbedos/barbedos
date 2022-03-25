from datetime import datetime
import functions_framework
from firebase_admin import firestore


JSON_KEY_PATH = (
    '/Users/barbe/Projects/barbedos/functions/ingest_file/'
    'key.serverless-admin.json')


@functions_framework.http
def ingest_file(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    def add_document_to_firestore(link, name):
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

    request_json = request.get_json(silent=True)
    if not request_json:
        return 'failed to get data'

    link = request_json.get('link')
    name = request_json.get('name')
    add_document_to_firestore(link, name)

    return f'Sucessfully received {name} - {link} added'
