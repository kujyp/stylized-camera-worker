import os


# CONTENT_BASE = "/media/ubuntu/a5d0dd63-d6a7-4d32-b068-0978b9fa66fb/data/content_data"
CONTENT_BASE = "data/content"
CONTENT_FILENAME = "chicago.jpg"
_CONTENT_NAME = os.path.splitext(CONTENT_FILENAME)[0]
_CONTENT_PATH = os.path.join(CONTENT_BASE, CONTENT_FILENAME)

# CKPT_BASE = "/media/ubuntu/a5d0dd63-d6a7-4d32-b068-0978b9fa66fb/data/trained_data"
CKPT_BASE = "data/ckpts"
OUTPUT_DIR = "data/outputs"

CONTENT_SHAPE = (1, 474, 712, 3)

def OUTPUT_PATH(style_name=""):
    import time
    timestr = time.strftime("%Y%m%d%H%M%S")

    filename = style_name + "_" + timestr + ".png"
    return os.path.join(OUTPUT_DIR, filename)
