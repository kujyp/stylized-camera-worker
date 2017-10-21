from config import config
from firebase.database.reference import get_listening_ref, get_working_ref
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

    my_stream = ref.stream(stream_handler)



def get_work_from_database(key, value):
    print("get_work_from_database")
    from config.config import get_worker_name
    value[config.DB.KEY_WORKER] = get_worker_name()
    from styletransfer.utils.timeutils import get_current_time
    value[config.DB.KEY_STARTEDAT] = get_current_time()
    get_working_ref().child(key).set(value)
    get_listening_ref().child(key).remove()


def process_data(key, value):
    if not Worker().is_working():
        get_work_from_database(key, value)
        downloadUrl = value[config.DB.KEY_DOWNLOADURL]
        path = value[config.DB.KEY_PATH]
        style_name = value[config.DB.KEY_STYLE_NAME]
        Worker().enqueue(downloadUrl, path, style_name)


def process_first_data(data):
    key = data[0]
    value = data[1]
    process_data(key, value)


def process_incoming_data(path, data):
    key = path[1:]
    process_data(key, data)