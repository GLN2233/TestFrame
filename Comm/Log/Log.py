import os
import logging
from Conf.config import log_cfg
from PIL import ImageGrab
import time

_BaseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

_log_level = eval(log_cfg['log_level'])
_log_path = log_cfg['log_path']
_log_format = log_cfg['log_format']

_log_file = os.path.join(_BaseHome, _log_path, 'log.txt')

from logging.handlers import TimedRotatingFileHandler


def log_init():
    logger = logging.getLogger('main')
    logger.setLevel(level=_log_level)
    formatter = logging.Formatter(_log_format)

    handler = TimedRotatingFileHandler(filename=_log_file, when="D", interval=1, backupCount=7)
    handler.setLevel(_log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(_log_level)
    console.setFormatter(formatter)
    logger.addHandler(console)


log_init()
logger = logging.getLogger('main')
logger.info('log test----------')

# 先定义截图文件的存放路径，这里在Log目录下建个Screen目录，按天存放截图
_today = time.strftime("%Y%m%d")
_screen_path = os.path.join(_BaseHome, _log_path, 'Screen', _today)


#再使用PIL的ImageGrab实现截图
def screen(name):
    t = time.time()
    png = ImageGrab.grab()
    if not os.path.exists(_screen_path):
        os.makedirs(_screen_path)
    image_name = os.path.join(_screen_path, name)
    png.save('%s_%s.png' % (image_name, str(round(t * 1000))))  # 文件名后面加了个时间戳，避免重名
