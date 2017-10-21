from config import config
from firebase.database.reference import get_working_ref, get_listening_ref, get_done_ref


def get_work_from_database(key, value):
    print("get_work_from_database")
    value[config.DB.KEY_WORKER] = config.get_worker_name()
    from styletransfer.utils.timeutils import get_current_time
    value[config.DB.KEY_STARTEDAT] = get_current_time()
    get_working_ref().child(key).set(value)
    get_listening_ref().child(key).remove()



def update_done_work_to_database(key, value, uploaded_url):
    print("update_done_work_to_database")
    value[config.DB.KEY_UPLOADEDURL] = uploaded_url
    from styletransfer.utils.timeutils import get_current_time
    value[config.DB.KEY_DONEAT] = get_current_time()
    get_done_ref().child(key).set(value)
    get_working_ref().child(key).remove()

def retrieve_uploaded_work():
    result = get_listening_ref().get()
    if result.each() is None:
        return None

    for each in result.each():
        return each.item