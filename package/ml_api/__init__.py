import sys
sys.path.insert(0, '')

import logging

from scania_truck.utils import helper

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(helper.get_console_handler())
logger.propagate = False