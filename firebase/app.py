from pyrebase import pyrebase

from auth.fb_account import config

firebase = pyrebase.initialize_app(config)

def getFirebase():
    return firebase

def getStorage():
    return firebase.storage()

def getDatabase():
    return firebase.database()