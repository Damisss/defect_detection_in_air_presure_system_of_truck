import logging

# from scania_truck.utils import config
from scania_truck_air_presure_fault_detector.utils import helper

# VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(helper.get_console_handler())
logger.propagate = False


# with open(VERSION_PATH, 'r') as version_file:
#     __version__ = version_file.read().strip()
