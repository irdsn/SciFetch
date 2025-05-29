##################################################################################################
#                                      SCRIPT OVERVIEW                                           #
#                                                                                                #
# This module interfaces with the Europe PMC API to retrieve academic articles related to        #
# a given query. It extracts metadata such as title, abstract, DOI, and publication date,        #
# returning them in a normalized dictionary format.                                              #
#                                                                                                #
# Classes:                                                                                       #
# - EuropePMCClient: Handles direct API communication and result formatting                      #
# - EuropePMCTool: LangChain-compatible wrapper for autonomous agent usage                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import requests
from typing import List, Dict
from utils.logs_config import logger

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class EuropePMCClient:
    """
    Client for querying the Europe PMC API and retrieving article metadata.

    This class sends search requests to the Europe PMC REST API and processes the JSON
    response to extract structured metadata including title, abstract, DOI, source,
    publication date, and article URL.

    Attributes:
        BASE_URL (str): Endpoint for the Europe PMC REST API.
    """

    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Searches the Europe PMC API for academic articles based on a free-text query.

        Extracts relevant metadata fields from each result and returns a list of normalized
        dictionaries. Fields include title, abstract, DOI, publication date, and a constructed URL.

        Args:
            query (str): Search query string to be submitted to the API.
            max_results (int): Maximum number of articles to return (default is 10).

        Returns:
            List[Dict]: List of dictionaries, each representing a scientific article.
        """

        logger.info(f"🔍 [EuropePMC] Launching search for query: {query}")
        params = {
            "query": query,
            "format": "json",
            "pageSize": max_results
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            logger.warning(f"⚠️ [EuropePMC] Request failed with status {response.status_code}")
            return []

        data = response.json()
        results = []
        for item in data.get("resultList", {}).get("result", []):
            results.append({
                "title": item.get("title", ""),
                "abstract": item.get("abstractText", ""),
                "doi": item.get("doi", ""),
                "source": "EuropePMC",
                "url": f"https://europepmc.org/article/{item.get('source', '')}/{item.get('id', '')}",
                "publication_date": item.get("firstPublicationDate", "")
            })
        return results

class EuropePMCTool:
    """
    LangChain-compatible wrapper for the EuropePMCClient.

    This tool exposes a callable interface to the Europe PMC search functionality,
    making it usable by autonomous agents or pipelines that rely on tool orchestration.

    Attributes:
        name (str): Identifier used for selecting the tool.
        description (str): Human-readable description for agent selection logic.
    """

    name = "europe_pmc_search"
    description = "Use this tool to find academic content from Europe PMC."

    def __call__(self, query: str) -> List[Dict]:
        """
        Executes a Europe PMC search using the provided query string.

        Args:
            query (str): Natural language search query.

        Returns:
            List[Dict]: Retrieved metadata entries from the Europe PMC API.
        """

        return EuropePMCClient().search(query)
