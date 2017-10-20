from config import config
from firebase.database import database
from ftp.ftpdownloader import downloadtraineddatafromftp, mkdir_unless_exist
from styletransfer.worker import feedfoward_with_url

mkdir_unless_exist(config.OUTPUT_DIR)
mkdir_unless_exist(config.CKPT_BASE)
mkdir_unless_exist(config.CONTENT_BASE)

downloaded_styles = downloadtraineddatafromftp(config.CKPT_BASE)
feedfoward_with_url("https://scontent-icn1-1.xx.fbcdn.net/v/t31.0-8/22459128_1676848559024079_955624277813855533_o.jpg?oh=f8463db22482524ca9c6748ac5ad40bd&oe=5A629DDB")
database()