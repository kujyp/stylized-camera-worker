import os

from config import config
from styletransfer.network.model import StyleModel
from styletransfer.utils.localstorage import get_img, generateFilenameWithTime, resize_img, save_img
from styletransfer.utils.remotestorage import downloadcontentfromurl


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

