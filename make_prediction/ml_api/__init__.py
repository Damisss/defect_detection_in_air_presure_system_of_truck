import logging

from scania_truck_air_presure_fault_detector.utils import helper

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(helper.get_console_handler())
logger.propagate = False
