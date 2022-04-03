import time
from google.cloud import compute_v1


PROJ = 'mythical-mason-137313'
INST = 'pimpbox'
ZONE = 'us-central1-a'
JSON_KEY_PATH = (
    '/Users/barbe/Projects/barbedos/'
    'key.compute_admin_barbedos.mythical-mason-137313.json'
)


def compute(_):
    op_client = compute_v1.ZoneOperationsClient()
    inst_client = compute_v1.InstancesClient()
    inst = inst_client.get(
        project=PROJ, zone=ZONE, instance=INST
    )
    if (inst.status == 'RUNNING'):
        return 'VM already running'

    opr = inst_client.start_unary(
        project=PROJ, zone=ZONE, instance=INST
    )
    start = time.time()
    while opr.status != compute_v1.Operation.Status.DONE:
        opr = op_client.wait(operation=opr.name, zone=ZONE, project=PROJ)
        if time.time() - start >= 300:  # 5 minutes
            raise TimeoutError()
    return 'VM Started'
