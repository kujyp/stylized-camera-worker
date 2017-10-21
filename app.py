from config import config
from firebase.database.listener import attach_listener_to_database
from firebase.database.styles import refresh_style_names
from ftp.ftpdownloader import downloadtraineddatafromftp, mkdir_unless_exist
from styletransfer.network.model import StyleModel
from styletransfer.worker import Worker


mkdir_unless_exist(config.OUTPUT_DIR)
mkdir_unless_exist(config.CKPT_BASE)
mkdir_unless_exist(config.CONTENT_BASE)
StyleModel()


print("Download styles")
style_names = downloadtraineddatafromftp(config.CKPT_BASE)
refresh_style_names(style_names)
Worker().load_downloaded_styles()
attach_listener_to_database()