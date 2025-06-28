##################################################################################################
#                                        NAME SANITIZER                                          #
#                                                                                                #
# Utility script to safely sanitize and normalize filenames for storing and retrieving PDF files #
# based on user-defined prompts. It removes unsafe characters, replaces spaces with underscores, #
# and ensures compatibility across filesystems and HTTP protocols.                               #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################
import re
import unicodedata

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def slugify_filename(text: str, max_length: int = 100) -> str:
    """
    Converts a given text string into a safe, ASCII-only filename slug.

    This function performs the following transformations:
    - Normalizes unicode characters to ASCII equivalents
    - Removes characters unsafe for filenames (e.g., quotes, symbols)
    - Replaces whitespace and dashes with underscores
    - Trims the result to a maximum length if needed

    Args:
        text (str): The input string to convert (e.g., a user prompt).
        max_length (int): Optional max length for the final filename.

    Returns:
        str: A sanitized, lowercase, underscore-based filename string.
    """
    # Normalize text (remove accents, symbols, smart quotes, etc.)
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")

    # Replace spaces and dashes with underscores
    ascii_text = re.sub(r"[ \t\-]+", "_", ascii_text)

    # Remove characters not allowed in filenames (e.g., slashes, quotes, symbols)
    ascii_text = re.sub(r"[^\w_.]", "", ascii_text)

    # Convert to lowercase
    slugified = ascii_text.lower()

    # Trim to maximum length (e.g., for filesystems like Windows)
    if len(slugified) > max_length:
        slugified = slugified[:max_length].rstrip("_")

    return slugified
