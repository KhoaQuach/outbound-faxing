"""
ob_logger.py:
    Define couple logging functions to use for the application to 
    log debug/error/info/warning messages
"""

import logging
import os

# set up logging to file 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/outbound_faxes.log',
                    filemode='a')

# Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

# Tell the handler to use this format
console.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger('outbound_faxes')

def debug(msg):
    if __debug__:
        logger.debug("(pid=" + str(os.getpid()) + ") " + msg)

def error(msg):
    logger.error("(pid=" + str(os.getpid()) + ") " + msg)

def info(msg):
    logger.info("(pid=" + str(os.getpid()) + ") " + msg)

def warning(msg):
    logger.warning("(pid=" + str(os.getpid()) + ") " + msg)
