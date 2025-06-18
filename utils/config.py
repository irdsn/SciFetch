##################################################################################################
#                                        OVERVIEW                                                #
#                                                                                                #
# This module defines shared configuration variables for the project.                            #
# It includes the default output directory used to save reports, logs, and images.               #
# Designed to centralize paths and simplify reuse across CLI and FastAPI components.             #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from pathlib import Path

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

# Option A: Save outputs to user's Downloads (recommended for deployed usage / FastAPI)
OUTPUT_DIR = Path.home() / "Downloads" / "SciFetch"

# Option B: Uncomment to save locally (for CLI / development)
# OUTPUT_DIR = Path("outputs")

# Ensure the directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
