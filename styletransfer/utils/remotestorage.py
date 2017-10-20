import os
import urllib.request

from styletransfer.utils.osutils import convert_path_sep, mkdir_unless_exist


def downloadcontentfromurl(url, contentdir, filename):
    contentdir = convert_path_sep(contentdir)

    # mkdir in local
    mkdir_unless_exist(contentdir)

    filepath = os.path.join(contentdir, filename)
    urllib.request.urlretrieve(url, filepath)