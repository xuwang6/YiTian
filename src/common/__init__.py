from src.common.adb import ADB
from src.common.log import Logger
from src.common.constants import LOG_PATH

adb = ADB()
log = Logger("YiTian", LOG_PATH).get_logger()
