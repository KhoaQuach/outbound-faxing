"""
ob_logger.py:
    Define couple logging functions to use for the application to 
    log debug/error/info/warning messages
"""

import logging
import os
import ob_global_vars

__author__      = ob_global_vars.AUTHORS
__copyright__   = ob_global_vars.COPYRIGHT
__credits__     = ob_global_vars.CREDITS
__license__     = ob_global_vars.LICENSE
__version__     = ob_global_vars.VERSION
__maintainer__  = ob_global_vars.MAINTAINER
__email__       = ob_global_vars.EMAIL
__status__      = ob_global_vars.STATUS

#
# Set up logging to file if at least DEBUG level logging
#
FORMAT='%(asctime)s [%(CMDID)s] - %(message)s'
logger=logging.getLogger("Outbound faxes")
fh=logging.handlers.RotatingFileHandler("/tmp/outbound_faxes.log",maxBytes=1024000,backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(fh)
logger.addFilter(ContextFilter())
logger.warning("WTH")

#
# Writes INFO messages or higher to the sys.stderr
#
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

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
