# -*- coding: utf-8 -*-

import logging as _logging, os as _os

logger = _logging.getLogger('xhamster')
logger.setLevel(_logging.DEBUG)

ch = _logging.StreamHandler()
ch.setLevel(_logging.DEBUG)

formatter = _logging.Formatter('[%(asctime)s] %(name)s %(module)s.%(funcName)s:%(lineno)s:%(levelname)s %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

basePath = _os.path.realpath(_os.path.join(_os.path.dirname(__file__), '..'))


