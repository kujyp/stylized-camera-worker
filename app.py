from config import config
from firebase.database import database
from ftp.ftpdownloader import downloadtraineddatafromftp, mkdir_unless_exist


mkdir_unless_exist(config.OUTPUT_DIR)
mkdir_unless_exist(config.CKPT_BASE)
mkdir_unless_exist(config.CONTENT_BASE)

downloaded_styles = downloadtraineddatafromftp(config.CKPT_BASE)
database()