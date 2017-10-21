from config import config
from firebase.app import Firebase


def get_style_ref():
    db = Firebase().get_database()
    return db.child(config.DB.REF_STYLES)

def get_listening_ref():
    db = Firebase().get_database()
    return db.child(config.DB.LISTENING_PATH)

def get_working_ref():
    db = Firebase().get_database()
    return db.child(config.DB.WORKING_PATH)

def get_root():
    return Firebase().get_database()