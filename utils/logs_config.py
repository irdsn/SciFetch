##################################################################################################
#                                        OVERVIEW                                                #
#                                                                                                #
# This module provides a preconfigured logger with color-coded output based on log severity.     #
# It is intended to be used across all project scripts to maintain consistent, readable logs.    #
# Uses the 'colorlog' library to apply different colors to DEBUG, INFO, WARNING, ERROR, and      #
# CRITICAL messages.                                                                             #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import logging                              # Logs and events
import colorlog                             # Logs and events

##################################################################################################
#                                       LOGGER CONFIGURATION                                     #
#                                                                                                #
# Configures the logger to display messages with different colors depending on the log level.    #
# Uses the colorlog library to differentiate between INFO, WARNING, ERROR, and CRITICAL levels.  #
##################################################################################################

# Define the color scheme for each log level
log_colors = {'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red'}

# Create a handler that uses ColorLogFormatter
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s%(levelname)s - %(message)s", log_colors=log_colors))

# Set up logger with the color handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)