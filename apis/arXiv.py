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
#                                        IMPLEMENTATION                                          #
##################################################################################################

class ArxivClient:
    """
    Interface for querying the arXiv API and retrieving structured scientific article metadata.

    This client sends a free-text search query to the arXiv API and parses the XML response
    using BeautifulSoup to extract standardized fields for each result. It is designed to
    integrate seamlessly with pipelines requiring structured scientific inputs.

    Attributes:
        BASE_URL (str): Base URL of the arXiv API endpoint.
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Searches the arXiv API for scientific articles matching a given free-text query.

        The results are parsed from XML and returned as a list of dictionaries with standardized keys,
        including title, abstract, DOI (if available), URL, publication date, and source.

        Args:
            query (str): Free-text search query to submit to arXiv.
            max_results (int): Maximum number of articles to retrieve (default is 10).

        Returns:
            List[Dict]: A list of articles, each represented as a dictionary with structured metadata.
        """

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

class ArxivTool:
    """
    LangChain-compatible wrapper for the ArxivClient.

    This tool provides a callable interface for use in LangChain autonomous agents.
    It exposes the arXiv search functionality via __call__ and implements _run for
    compatibility. Async execution (_arun) is not supported.

    Attributes:
        name (str): Tool identifier used by LangChain.
        description (str): Description used to guide agent tool selection.
    """

    name = "arxiv_search"
    description = "Use this tool to find titles and abstracts from arXiv based on a query. Returns structured JSON."

    def __call__(self, query: str) -> List[Dict]:
        """
        Invokes the arXiv search using the provided query.

        Args:
            query (str): Free-text query string.

        Returns:
            List[Dict]: List of articles matching the query.
        """

        return ArxivClient().search(query=query)

    def _run(self, query: str):
        """
        Synchronous execution wrapper for LangChain compatibility.

        Args:
            query (str): The query to be passed to the arXiv client.

        Returns:
            List[Dict]: List of articles returned by the client.
        """

        return self.__call__(query)

    def _arun(self, query: str):
        """
        Placeholder for asynchronous execution (not implemented).

        Raises:
            NotImplementedError: Asynchronous calls are not supported for this tool.
        """

        raise NotImplementedError("Async not supported for ArxivTool.")
