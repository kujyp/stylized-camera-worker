import os
import queue

from config import config
from styletransfer.network.model import StyleModel
from styletransfer.utils.localstorage import get_img, generateFilenameWithTime, resize_img, save_img, get_dirnames
from styletransfer.utils.remotestorage import downloadcontentfromurl
from styletransfer.utils.singleton import Singleton


class Worker(metaclass=Singleton):
    _is_working = False

    def __init__(self):
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

    def enqueue(self, downloadUrl, path, style_name):
        self.working_queue.put((downloadUrl, path, style_name))
        print("Worker/enqueue downloadUrl=%s, path=%s" % (downloadUrl, path))
        if self._is_working is True:
            print("enqueue/_is_working is True")
            return
        else:
            self.activate_worker()

    def does_style_exist(self, style_name):
        if style_name in self.styles:
            return True
        return False

    def activate_worker(self):
        print('activate_worker')
        if self._is_working:
            print('activate_worker/is working')
            return
        else:
            self._is_working = True
            while True:
                downloadUrl, path, style_name = self.working_queue.get()
                print('activate_worker/downloadUrl = %s, styleName = %s' % (downloadUrl, style_name))
                output_filepath = self.feedfoward(downloadUrl, style_name)
                print('activate_worker/Task done output_filepath = %s' % output_filepath)
                if self.working_queue.empty():
                    print('activate_worker/working_queue is empty')
                    break

            # notify listener "retrieve db"
            self._is_working = False


def feedfoward(image_url, style):
    filename = generateFilenameWithTime()
    downloadcontentfromurl(image_url, config.CONTENT_BASE, filename)
    filepath = os.path.join(config.CONTENT_BASE, filename)
    content_img = get_img(filepath)
    resized_img = resize_img(content_img)

    StyleModel().load_style(style)

    output_img = StyleModel().feedfoward(resized_img)

    output_filepath = os.path.join(config.OUTPUT_DIR, filename)
    save_img(output_filepath, output_img[0])

    return output_filepath

