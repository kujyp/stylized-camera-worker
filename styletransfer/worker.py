import os
import queue

from config import config
from firebase.database.workdao import update_done_work_to_database
from firebase.storage.uploader import upload_to_storage
from styletransfer.network.model import StyleModel
from styletransfer.utils.localstorage import get_img, generate_filename_with_time, resize_img, save_img, get_dirnames
from styletransfer.utils.remotestorage import downloadcontentfromurl
from styletransfer.utils.singleton import Singleton


class Worker(metaclass=Singleton):
    class Listener():
        def __init__(self, action) -> None:
            super().__init__()
            self.action = action

        def activate(self):
            print("Listener,activate/action type = %s" % self.action)
            if self.action:
                self.action()

    def __init__(self):
        self._is_working = False
        self.listener = None
        self.working_queue = queue.Queue()

    def load_downloaded_styles(self):
        self.styles = get_dirnames(config.CKPT_BASE)

    def feedfoward(self, image_url, style_name):
        if self.does_style_exist(style_name):
            return feedfoward(image_url, style_name)

        else:
            return None

    def is_working(self):
        return self._is_working

    def enqueue(self, download_url, path, style_name, key, value):
        self.working_queue.put((download_url, path, style_name, key, value))
        print("Worker/enqueue downloadUrl=%s, path=%s" % (download_url, path))
        if self._is_working is True:
            print("enqueue/_is_working is True")
            return
        else:
            self.activate_worker()

    def does_style_exist(self, style_name):
        if style_name in self.styles:
            return True
        return False

    def set_listener(self, listener):
        self.listener = listener


    def activate_worker(self):
        print('activate_worker')
        if self._is_working:
            print('activate_worker/is working')
            return
        else:
            self._is_working = True
            while True:
                download_url, path, style_name, key, value = self.working_queue.get()
                print('activate_worker/downloadUrl = %s, styleName = %s' % (download_url, style_name))
                output_filepath = self.feedfoward(download_url, style_name)
                print('activate_worker/Task done output_filepath = %s' % output_filepath)

                uploaded_url = upload_to_storage(output_filepath)
                update_done_work_to_database(key, value, uploaded_url)
                if self.working_queue.empty():
                    print('activate_worker/working_queue is empty')
                    break

            # notify listener "retrieve db"
            self._is_working = False
            self.notify_listener_to_retrieve_db()

    def notify_listener_to_retrieve_db(self):
        if self.listener:
            self.listener.activate()



def feedfoward(image_url, style):
    filename = style + "_" + generate_filename_with_time()
    downloadcontentfromurl(image_url, config.CONTENT_BASE, filename)
    filepath = os.path.join(config.CONTENT_BASE, filename)
    content_img = get_img(filepath)
    resized_img = resize_img(content_img)

    StyleModel().load_style(style)

    output_img = StyleModel().feedfoward(resized_img)

    output_filepath = os.path.join(config.OUTPUT_DIR, filename)
    save_img(output_filepath, output_img[0])

    return filename

