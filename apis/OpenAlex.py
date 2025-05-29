##################################################################################################
#                                        OPENALEX API CLIENT                                     #
#                                                                                                #
# This script connects to the OpenAlex API to retrieve academic publications matching a query.   #
# It formats and returns a unified response format with metadata such as title, DOI, and date.   #
#                                                                                                #
# The client handles decoding of the abstract stored as an inverted index.                       #
##################################################################################################

import requests
from typing import List, Dict

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class OpenAlexClient:
    """
    Client for querying the OpenAlex API to retrieve academic publication metadata.

    This class sends search queries to OpenAlex and extracts structured metadata from
    the response. It also handles decoding of abstracts stored in inverted index format.

    Attributes:
        BASE_URL (str): Base URL for the OpenAlex API endpoint.
    """

    BASE_URL = "https://api.openalex.org/works"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Searches the OpenAlex API for publications matching a query.

        Extracts key fields such as title, abstract, DOI, source, URL, and publication date.
        Abstracts are decoded from OpenAlex's inverted index format using `decode_abstract`.

        Args:
            query (str): Free-text search query.
            max_results (int): Number of results to retrieve (default is 10).

        Returns:
            List[Dict]: A list of structured metadata dictionaries for each publication.
        """

        params = {
            "search": query,
            "per_page": max_results,
            "sort": "publication_date:desc"
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []

        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "abstract": self.decode_abstract(item),
                "doi": item.get("doi", ""),
                "source": "OpenAlex",
                "url": item.get("id", ""),
                "publication_date": item.get("publication_date", "")
            })

        return results

    def decode_abstract(self, item: Dict) -> str:
        """
        Decodes an abstract stored in OpenAlex's inverted index format.

        The inverted index maps each word to a list of positions. This method reconstructs
        the abstract string by ordering the words according to their position in the index.

        Args:
            item (Dict): A single result item from the OpenAlex API.

        Returns:
            str: Decoded abstract string, or empty string if no abstract is available.
        """

        inverted = item.get("abstract_inverted_index")
        if not inverted:
            return ""
        word_positions = {pos: word for word, positions in inverted.items() for pos in positions}
        abstract = " ".join(word_positions.get(i, "") for i in range(max(word_positions.keys()) + 1))
        return abstract

class OpenAlexTool:
    """
    LangChain-compatible wrapper for the OpenAlexClient.

    This tool provides a callable interface for querying OpenAlex and retrieving
    academic publication metadata. Designed for use in autonomous agent frameworks.

    Attributes:
        name (str): Identifier for the tool within the LangChain agent environment.
        description (str): Description used for agent tool selection and reasoning.
    """

    name = "openalex_search"
    description = "Use this tool to find titles and abstracts from OpenAlex based on scientific queries."

    def __call__(self, query: str) -> List[Dict]:
        """
        Executes a publication search on OpenAlex using the provided query.

        Args:
            query (str): Free-text scientific query.

        Returns:
            List[Dict]: List of publication metadata entries from OpenAlex.
        """

        return OpenAlexClient().search(query)
