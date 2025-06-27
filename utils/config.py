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

import os
from pathlib import Path

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

if os.getenv("RENDER", False):
    # Option A :Use a Render-safe temp directory
    OUTPUT_DIR = Path("/tmp") / "scifetch_outputs"
else:
    # Option B: Save outputs to user's Downloads (recommended for local deployed usage / FastAPI)
    OUTPUT_DIR = Path.home() / "Downloads" / "SciFetch"

    # Option C: Uncomment to save locally (for CLI / development)
    # OUTPUT_DIR = Path("outputs")

# Ensure the directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
