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
#                                 OPENALEX API CLIENT                                            #
#                                                                                                #
# Queries the OpenAlex API and extracts the results in a standardized format.                    #
#                                                                                                #
# :param query: Search string to send to the OpenAlex API                                        #
# :param max_results: Number of results to retrieve                                              #
# :return: List of formatted documents with title, abstract, doi, etc.                           #
##################################################################################################

class OpenAlexClient:
    BASE_URL = "https://api.openalex.org/works"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
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

##################################################################################################
#                             DECODE ABSTRACT FROM INVERTED INDEX                                #
#                                                                                                #
# Reconstructs the abstract string from OpenAlex's inverted index representation.                #
#                                                                                                #
# :param item: A single publication result from OpenAlex API                                     #
# :return: Decoded abstract string                                                               #
##################################################################################################

    def decode_abstract(self, item: Dict) -> str:
        inverted = item.get("abstract_inverted_index")
        if not inverted:
            return ""
        word_positions = {pos: word for word, positions in inverted.items() for pos in positions}
        abstract = " ".join(word_positions.get(i, "") for i in range(max(word_positions.keys()) + 1))
        return abstract

##################################################################################################
#                                   OPENALEX TOOL WRAPPER                                        #
#                                                                                                #
# LangChain-compatible wrapper that enables calling the OpenAlexClient as a tool.                #
#                                                                                                #
# :param query: Search query string                                                              #
# :return: List of results from OpenAlex                                                         #
##################################################################################################

class OpenAlexTool:
    name = "openalex_search"
    description = "Use this tool to find titles and abstracts from OpenAlex based on scientific queries."

    def __call__(self, query: str) -> List[Dict]:
        return OpenAlexClient().search(query)
