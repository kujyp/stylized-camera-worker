from pyrebase import pyrebase

from auth.accounts import FIREBASE
from styletransfer.utils.singleton import Singleton


class Firebase(metaclass=Singleton):
    def __init__(self):
        self._firebase = pyrebase.initialize_app(FIREBASE.config)
        self._storage = None
        self._database = None

    def get_firebase(self):
        return self._firebase

    def get_storage(self):
        if self._storage is None:
            print("Firebase/Initialize storage")
            self._storage = self._firebase.storage()

        return self._storage

    def get_database(self):
        if self._database is None:
            print("Firebase/Initialize database")
            self._database = self._firebase.database()

        return self._database