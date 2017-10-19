LISTENING_PATH = "uploaded_tasks"
KEY_DOWNLOADURL = 'downloadUrl'
KEY_PATH = 'path'

def database():
    from firebase.app import getDatabase
    db = getDatabase()
    ref = db.child(LISTENING_PATH)
    def stream_handler(message):
        print("Message %s" % message)
        print("Event %s" % message["event"])
        print("Path %s" % message["path"])
        data = dict(message["data"])
        for idx, key in enumerate(data.keys()):
            value = dict(data.get(key))
            print("Data %02d %s" % (idx, key))  # {'title': 'Pyrebase', "body": "etc..."}
            print("Value / downloadUrl = %s, path = %s" % (value[KEY_DOWNLOADURL], value[KEY_PATH]))

    my_stream = ref.stream(stream_handler)