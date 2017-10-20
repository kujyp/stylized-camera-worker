from pyrebase import pyrebase

from auth.accounts import FIREBASE

firebase = pyrebase.initialize_app(FIREBASE.config)

def getFirebase():
    return firebase

def getStorage():
    return firebase.storage()

def getDatabase():
    return firebase.database()