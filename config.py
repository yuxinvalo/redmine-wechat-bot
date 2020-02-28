import logging
import logging.config

logging.config.fileConfig("logger.ini")
logger = logging.getLogger("redmine-wechat-watcher")