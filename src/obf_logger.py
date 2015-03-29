"""
obf_logger.py:
    Define couple logging functions to use for the application to 
    log debug/error/info/warning messages
"""

import logging
import logging.handlers
import os
import obf_global_vars

__author__      = obf_global_vars.AUTHORS
__copyright__   = obf_global_vars.COPYRIGHT
__credits__     = obf_global_vars.CREDITS
__license__     = obf_global_vars.LICENSE
__version__     = obf_global_vars.VERSION
__maintainer__  = obf_global_vars.MAINTAINER
__email__       = obf_global_vars.EMAIL
__status__      = obf_global_vars.STATUS

#
# Set up logging to file if at least DEBUG level logging
#
FORMAT = '%(name)-12s: %(asctime)s %(levelname)-8s %(message)s'
fh = logging.handlers.RotatingFileHandler(obf_global_vars.OBF_LOG_FILE, maxBytes=1024000, backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger("Outbound faxes")
logger.addHandler(fh)

#
# Writes INFO messages or higher to the sys.stderr
#
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Set a format which is simpler for console use
formatter = logging.Formatter(FORMAT)

# Tell the handler to use this format
console.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(console)

def debug(msg):
    if __debug__:
        logger.debug("(pid=" + str(os.getpid()) + ") " + msg)

def error(msg):
    logger.error("(pid=" + str(os.getpid()) + ") " + msg)

def info(msg):
    logger.info("(pid=" + str(os.getpid()) + ") " + msg)

def warning(msg):
    logger.warning("(pid=" + str(os.getpid()) + ") " + msg)
