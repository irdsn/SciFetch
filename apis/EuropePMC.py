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
#                                     EUROPE PMC CLIENT                                          #
#                                                                                                #
# Interacts with the Europe PMC API to fetch article metadata.                                   #
# Returns normalized fields across all results.                                                  #
#                                                                                                #
# :param query: Search string to query in the EuropePMC API                                      #
# :param max_results: Maximum number of results to return                                        #
# :return: List of dictionaries with normalized article metadata                                 #
##################################################################################################

class EuropePMCClient:
    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
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

##################################################################################################
#                                        EUROPE PMC TOOL                                         #
#                                                                                                #
# Tool wrapper for LangChain-like agents to invoke search functionality of EuropePMC.            #
#                                                                                                #
# :param query: Natural language query to pass to the search function                            #
# :return: List of article metadata results                                                      #
##################################################################################################

class EuropePMCTool:
    name = "europe_pmc_search"
    description = "Use this tool to find academic content from Europe PMC."

    def __call__(self, query: str) -> List[Dict]:
        return EuropePMCClient().search(query)
