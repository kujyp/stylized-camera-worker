import numpy as np
import scipy.misc


def get_img(src, img_size=False):
    img = scipy.misc.imread(src, mode='RGB')  # misc.imresize(, (256, 256, 3))
    if not (len(img.shape) == 3 and img.shape[2] == 3):
        img = np.dstack((img, img, img))
    if img_size != False:
        img = scipy.misc.imresize(img, img_size)
    return img

def save_img(src, img):
    img = np.clip(img, 0, 255).astype(np.uint8)
    scipy.misc.imsave(src, img)

def generateFilenameWithTime():
    import time
    timestr = time.strftime("%Y%m%d%H%M%S") + "_" + str(time.clock())[-2:]
    filename = timestr + ".png"
    return filename