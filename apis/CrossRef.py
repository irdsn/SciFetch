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
#                                 EXTRACT PUBLICATION DATE                                       #
#                                                                                                #
# Extracts a clean YYYY-MM-DD publication date string from CrossRef metadata.                    #
# Handles different date fields like "published-online", "created", etc.                        #
# If the date refers to a future year, it's marked as not-yet-published.                         #
#                                                                                                #
# :param item: A dictionary from a CrossRef API response                                         #
# :return: ISO formatted date string or warning placeholder                                      #
##################################################################################################

def extract_crossref_date(item: dict) -> str:
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

##################################################################################################
#                                       CROSSREF CLIENT                                          #
#                                                                                                #
# Handles querying the CrossRef API and structuring response metadata.                          #
# It filters, cleans, and normalizes fields like title, DOI, and abstract.                      #
##################################################################################################

class CrossRefClient:
    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
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

    ##################################################################################################
    #                                      CLEAN ABSTRACT                                            #
    #                                                                                                #
    # Removes XML/HTML tags (e.g., <jats:p>) from abstract fields.                                   #
    # Returns clean, plain text abstracts.                                                           #
    ##################################################################################################

    def _clean_abstract(self, raw_abstract: str) -> str:
        if not raw_abstract:
            return ""
        cleaned = re.sub(r"<[^>]+>", "", raw_abstract)
        return cleaned.strip()

##################################################################################################
#                                        CROSSREF TOOL                                           #
#                                                                                                #
# LangChain-compatible wrapper tool for CrossRef search client.                                   #
# This enables future autonomous agent-based selection and orchestration.                         #
##################################################################################################

class CrossRefTool:
    name = "crossref_search"
    description = "Use this tool to find metadata of academic publications from CrossRef."

    def __call__(self, query: str) -> List[Dict]:
        return CrossRefClient().search(query)

    def _run(self, query: str):
        return self.__call__(query)

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported for CrossRefTool.")
