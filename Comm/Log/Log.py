import os
import logging
from Conf.Config import log_cfg

_BaseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

_log_level = eval(log_cfg['log_level'])
_log_path = log_cfg['log_path']
_log_format = log_cfg['log_format']

_log_file = os.path.join(_BaseHome, _log_path, 'log.txt')
