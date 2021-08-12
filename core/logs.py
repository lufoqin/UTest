import os
import logzero
import logging
from configs import settings
from concurrent_log_handler import ConcurrentRotatingFileHandler


class CustomLogger(object):

    def __init__(self, level=settings.log_devel, filename='autotest.log'):
        # if not isinstance(logging.)
        self.logfile = os.path.join(settings.log_path, filename)
        file_path = os.path.split(self.logfile)[0]
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        formatter = logging.Formatter('%(asctime)-15s - [%(filename)s: %(lineno)s] - %(levelname)s: %(message)s')
        rotating_filehandler = ConcurrentRotatingFileHandler(self.logfile,
                                                             maxBytes=settings.log_max_size,
                                                             backupCount=settings.log_backup_count,
                                                             encoding='utf-8')
        rotating_filehandler.setLevel(level)
        rotating_filehandler.setFormatter(formatter)

        self.logger = logzero.setup_logger(name=filename)
        self.logger.addHandler(rotating_filehandler)


log = CustomLogger().logger


if __name__ == "__main__":
    log.info("testtest")
