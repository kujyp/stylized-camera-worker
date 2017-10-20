import os

from config import config
from styletransfer.utils.localstorage import get_img, generateFilenameWithTime
from styletransfer.utils.remotestorage import downloadcontentfromurl


def feedfoward_with_url(image_url):
    filename = generateFilenameWithTime()
    downloadcontentfromurl(image_url, config.CONTENT_BASE, filename)
    filepath = os.path.join(config.CONTENT_BASE, filename)
    content_img = get_img(filepath)

    print(content_img)