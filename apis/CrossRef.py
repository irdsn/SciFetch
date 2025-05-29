##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module provides a client and tool wrapper to fetch metadata of scientific publications    #
# from the CrossRef API based on a search query. It processes and filters results for structure  #
# and clarity. Intended for integration within larger retrieval pipelines or agent frameworks.   #
#                                                                                                #
# Key Features:                                                                                  #
# - Cleans and parses CrossRef abstracts                                                         #
# - Filters out future-dated or placeholder documents                                            #
# - Provides structured output compatible with multi-source aggregation                          #
##################################################################################################

##################################################################################################
#                                             IMPORTS                                            #
##################################################################################################

import requests
import re
from typing import List, Dict
from datetime import datetime
from utils.logs_config import logger

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def extract_crossref_date(item: dict) -> str:
    """
    Extracts and formats the publication date from a CrossRef item.

    Tries multiple fields (e.g., 'published-online', 'published-print', 'created') to locate a date.
    If the extracted year is in the future, the article is flagged as not yet published.

    Args:
        item (dict): A single record from the CrossRef API response.

    Returns:
        str: Formatted date in 'YYYY-MM-DD' format, or a warning message if unpublished.
    """

    current_year = datetime.utcnow().year
    for key in ["published-online", "published-print", "created"]:
        date_data = item.get(key, {}).get("date-parts", [])
        if date_data and len(date_data[0]) >= 1:
            parts = date_data[0]
            year = parts[0]
            month = parts[1] if len(parts) > 1 else 1
            day = parts[2] if len(parts) > 2 else 1

            if year > current_year:
                return "This is an accepted article with a DOI pre-assigned that is not yet published."

            return f"{year:04d}-{month:02d}-{day:02d}"

    return ""

class CrossRefClient:
    """
    Client for querying the CrossRef API and parsing publication metadata.

    Sends a search request to CrossRef and processes the response by cleaning
    abstracts and filtering incomplete or placeholder entries. Extracted inputs
    includes title, abstract, DOI, URL, source, and publication date.

    Attributes:
        BASE_URL (str): Base URL for the CrossRef API endpoint.
    """

    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Queries the CrossRef API for scientific publications matching a search string.

        Filters out articles with missing or placeholder titles. Cleans abstracts
        and extracts consistent metadata fields suitable for downstream integration.

        Args:
            query (str): Free-text search string.
            max_results (int): Maximum number of results to return (default is 10).

        Returns:
            List[Dict]: List of structured publication metadata dictionaries.
        """

        logger.info(f"[CrossRef] 🔍 Launching search for query: {query}")

        params = {
            "query": query,
            "rows": max_results,
            "sort": "published",
            "order": "desc",
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            logger.warning(f"[CrossRef] ⚠️ Request failed with status {response.status_code}")
            return []

        data = response.json()
        results = []

        for item in data.get("message", {}).get("items", []):
            title = item.get("title", [""])[0]
            abstract = self._clean_abstract(item.get("abstract", ""))
            publication_date = extract_crossref_date(item)

            if not title or title.lower().startswith("title pending"):
                continue

            results.append({
                "title": title,
                "abstract": abstract,
                "doi": item.get("DOI", ""),
                "source": "CrossRef",
                "url": f"https://doi.org/{item.get('DOI', '')}",
                "publication_date": publication_date
            })

        return results

    def _clean_abstract(self, raw_abstract: str) -> str:
        """
        Cleans XML or HTML tags from raw abstract strings.

        Intended to convert raw markup-heavy abstracts (e.g., <jats:p>) into plain text.

        Args:
            raw_abstract (str): Abstract string potentially containing XML/HTML tags.

        Returns:
            str: Cleaned plain text abstract.
        """

        if not raw_abstract:
            return ""
        cleaned = re.sub(r"<[^>]+>", "", raw_abstract)
        return cleaned.strip()

class CrossRefTool:
    """
    LangChain-compatible wrapper for the CrossRefClient.

    This class exposes a simple callable interface for retrieving metadata
    from CrossRef, enabling use in autonomous agent pipelines. Supports sync
    execution only.

    Attributes:
        name (str): Identifier for LangChain agent selection.
        description (str): Tool description shown to the agent.
    """

    name = "crossref_search"
    description = "Use this tool to find metadata of academic publications from CrossRef."

    def __call__(self, query: str) -> List[Dict]:
        """
        Executes a CrossRef metadata search using the given query.

        Args:
            query (str): Search query for scientific literature.

        Returns:
            List[Dict]: List of publication metadata entries.
        """

        return CrossRefClient().search(query)

    def _run(self, query: str):
        """
        Synchronous wrapper for tool execution in LangChain environments.

        Args:
            query (str): The query string to be passed to the client.

        Returns:
            List[Dict]: Retrieved metadata from CrossRef.
        """

        return self.__call__(query)

    def _arun(self, query: str):
        """
        Async placeholder method for LangChain integration.

        Raises:
            NotImplementedError: Asynchronous execution is not supported.
        """

        raise NotImplementedError("Async not supported for CrossRefTool.")
