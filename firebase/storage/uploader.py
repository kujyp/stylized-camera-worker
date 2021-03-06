from config import config
from firebase.app import Firebase
from styletransfer.utils.localstorage import remove_file


def path_join_on_firebase_storage(path1, path2):
    return path1 + "/" + path2


def upload_to_storage(filename):
    storage = Firebase().get_storage()
    path = path_join_on_firebase_storage(config.STORAGE.DONE_PATH, filename)
    import os
    localpath = os.path.join(config.OUTPUT_DIR, filename)
    storage.child(path).put(localpath)
    url = storage.child(path).get_url(False)
    print("upload_to_storage/url = %s" % url)

    remove_file(localpath)

    return url