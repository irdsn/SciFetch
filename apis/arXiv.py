##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script provides an interface to query the arXiv API and return scientific articles        #
# matching a user-defined query. It extracts relevant metadata and returns it in a unified       #
# structure suitable for use in LangChain agents or other pipelines.                             #
#                                                                                                #
# Key Features:                                                                                  #
# - Queries arXiv's API with free-text search.                                                   #
# - Parses XML response using BeautifulSoup.                                                     #
# - Returns structured fields: title, abstract, doi, url, source, and publication_date.          #
# - Contains a LangChain-compatible Tool wrapper class.                                          #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import requests
from typing import List, Dict
from bs4 import BeautifulSoup

##################################################################################################
#                                         ARXIV CLIENT                                           #
#                                                                                                #
# Queries the arXiv API and parses results to extract clean, structured data fields.             #
#                                                                                                #
# :param query: Free-text string for article search.                                             #
# :param max_results: Maximum number of articles to return.                                      #
# :return: List of dictionaries, one per article with standardized keys.                         #
##################################################################################################

class ArxivClient:
    BASE_URL = "http://export.arxiv.org/api/query"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "xml")
        entries = soup.find_all("entry")
        results = []

        for entry in entries:
            title = entry.title.get_text(strip=True)
            abstract = entry.summary.get_text(strip=True)
            url = entry.id.get_text(strip=True)
            doi_tag = entry.find("arxiv:doi")
            doi = doi_tag.get_text(strip=True) if doi_tag else ""

            results.append({
                "title": title,
                "abstract": abstract,
                "doi": doi,
                "source": "arXiv",
                "url": url,
                "publication_date": entry.published.get_text(strip=True).split("T")[0] if entry.published else ""
            })

        return results

##################################################################################################
#                                     LANGCHAIN TOOL WRAPPER                                     #
#                                                                                                #
# Wraps ArxivClient in a callable interface suitable for use with LangChain agents.              #
# Implements required __call__, _run, and _arun methods.                                         #
#                                                                                                #
# :param query: The search query string passed to the client.                                    #
# :return: List of articles returned by the client.                                              #
##################################################################################################

class ArxivTool:
    name = "arxiv_search"
    description = "Use this tool to find titles and abstracts from arXiv based on a query. Returns structured JSON."

    def __call__(self, query: str) -> List[Dict]:
        client = ArxivClient()
        return client.search(query=query)

    def _run(self, query: str):
        return self.__call__(query)

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported for ArxivTool.")
