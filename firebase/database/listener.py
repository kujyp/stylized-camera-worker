from config import config
from firebase.database.reference import get_listening_ref, get_working_ref
from firebase.database.workdao import get_work_from_database, retrieve_uploaded_work
from styletransfer.worker import Worker


def attach_listener_to_database():
    ref = get_listening_ref()

    def stream_handler(message):
        event = message["event"]
        path = message["path"]
        print("Message %s" % message)
        print("Event %s" % event)
        if event == config.DB.Event_PUT:
            data = message["data"]
            if data is None:
                # DELETED
                print("Data is None")
                return

            if path == config.DB.Path_ROOT:
                firstitem = data.popitem()
                process_first_data(firstitem)
            else:
                process_incoming_data(path, data)

    Worker().set_listener(Worker.Listener(retrieve_data))
    my_stream = ref.stream(stream_handler)

def retrieve_data():
    print("retrieve_data/")
    item = retrieve_uploaded_work()
    if item is not None:
        process_first_data(item)


def process_data(key, value):
    if not Worker().is_working():
        get_work_from_database(key, value)
        downloadUrl = value[config.DB.KEY_DOWNLOADURL]
        path = value[config.DB.KEY_PATH]
        style_name = value[config.DB.KEY_STYLE_NAME]
        Worker().enqueue(downloadUrl, path, style_name, key, value)


def process_first_data(data):
    key = data[0]
    value = data[1]
    process_data(key, value)


def process_incoming_data(path, data):
    key = path[1:]
    process_data(key, data)
