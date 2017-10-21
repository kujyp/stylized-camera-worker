

# CONTENT_BASE = "/media/ubuntu/a5d0dd63-d6a7-4d32-b068-0978b9fa66fb/data/content_data"
CONTENT_BASE = "data/content"

# CKPT_BASE = "/media/ubuntu/a5d0dd63-d6a7-4d32-b068-0978b9fa66fb/data/trained_data"
CKPT_BASE = "data/ckpts"
OUTPUT_DIR = "data/outputs"
CONFIG_DIR = "config"
WORKER_CONFIG = "worker.txt"

CONTENT_SHAPE = (1, 474, 712, 3)
IMAGE_SIZE = CONTENT_SHAPE[1:3]

# FIREBASE DATABASE
class DB:
    REF_STYLES = "styles"

    LISTENING_PATH = "uploaded_tasks"
    WORKING_PATH = "working_tasks"
    DONE_PATH = 'done_tasks'
    KEY_UPLOADEDURL = "uploadedUrl"
    KEY_DONEAT = "doneAt"
    KEY_DOWNLOADURL = 'downloadUrl'
    KEY_PATH = 'path'
    KEY_WORKER = 'worker'
    KEY_STARTEDAT = 'startedAt'
    KEY_STYLE_NAME = 'styleName'
    Event_PUT = "put"
    Path_ROOT = "/"

class STORAGE:
    DONE_PATH = "done_images"

def get_worker_name():
    import os
    worker_config_path = os.path.join(CONFIG_DIR, WORKER_CONFIG)

    if os.path.isfile(worker_config_path):
        worker_config = open(worker_config_path, "r")
        print("Loading Worker name from %s ..." % worker_config_path)
        worker_name = worker_config.readline()
        worker_config.close()
    else:
        worker_config = open(worker_config_path, "w")
        worker_name = input("Worker name ? ")
        worker_name.replace(' ', '')
        worker_config.write(worker_name)
        worker_config.close()

    return worker_name