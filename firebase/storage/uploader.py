from config import config
from firebase.app import Firebase


def path_join_on_firebase_storage(path1, path2):
    return path1 + "/" + path2


def upload_to_storage(filename):
    storage = Firebase().get_storage()
    path = path_join_on_firebase_storage(config.STORAGE.DONE_PATH, filename)
    storage.child(path).put(filename)
    url = storage.child(path).get_url(False)
    print("upload_to_storage/url = %s" % url)

    return url