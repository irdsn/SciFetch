##################################################################################################
#                                        PUBMED API CLIENT                                       #
#                                                                                                #
# This script provides functionality to search and fetch scientific articles from PubMed.        #
# It exposes a client class and a LangChain tool wrapper for autonomous integration.             #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from dateutil import parser

##################################################################################################
#                                  EXTRACT PUBMED DATE                                           #
#                                                                                                #
# Attempts to extract a publication date from a PubMed article using various strategies.         #
# Returns the date in format YYYY-MM-DD or YYYY-MM, or empty string if unavailable.              #
#                                                                                                #
# :param article: BeautifulSoup-parsed PubMedArticle element                                     #
# :return: publication date string                                                               #
##################################################################################################

def extract_pubmed_date(article) -> str:
    try:
        if article.MedlineCitation.Article.ArticleDate:
            y = article.MedlineCitation.Article.ArticleDate.Year.get_text()
            m = article.MedlineCitation.Article.ArticleDate.Month.get_text()
            d = article.MedlineCitation.Article.ArticleDate.Day.get_text()
            return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
    except Exception:
        pass

    try:
        completed = article.MedlineCitation.DateCompleted
        y = completed.Year.get_text()
        m = completed.Month.get_text()
        return f"{y}-{m.zfill(2)}-01"
    except Exception:
        pass

    try:
        date_str = article.MedlineCitation.Article.Journal.JournalIssue.PubDate.MedlineDate.get_text()
        dt = parser.parse(date_str, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    return ""

##################################################################################################
#                                      PUBMED CLIENT                                             #
#                                                                                                #
# Searches articles using the PubMed API and fetches article metadata from article IDs.          #
#                                                                                                #
# :method search: Executes a query against PubMed and returns a list of matching IDs             #
# :method fetch_details: Uses efetch API to retrieve metadata for given IDs                      #
##################################################################################################

class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def search(self, query: str, max_results: int = 10) -> List[str]:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "pub+date"
        }
        resp = requests.get(self.BASE_URL, params=params)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("esearchresult", {}).get("idlist", [])
        return []

    def fetch_details(self, ids: List[str]) -> List[Dict]:
        if not ids:
            return []
        params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml"
        }
        resp = requests.get(self.FETCH_URL, params=params)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "xml")
        articles = []
        for article in soup.find_all("PubmedArticle"):
            title = article.Article.ArticleTitle.get_text(strip=True) if article.Article.ArticleTitle else None
            abstract = article.Article.Abstract.AbstractText.get_text(strip=True) if article.Article.Abstract else None
            article_id = article.MedlineCitation.PMID.get_text(strip=True)
            doi_tag = article.find("ELocationID", {"EIdType": "doi"})
            doi = doi_tag.get_text(strip=True) if doi_tag else None
            pub_date = extract_pubmed_date(article)

            articles.append({
                "title": title,
                "abstract": abstract,
                "doi": doi,
                "source": "PubMed",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}",
                "publication_date": pub_date
            })
        return articles

##################################################################################################
#                                       PUBMED TOOL                                              #
#                                                                                                #
# LangChain-compatible wrapper for using PubMed search as a tool.                                #
##################################################################################################

class PubMedTool:
    name = "pubmed_search"
    description = "Use this tool to find titles and abstracts from PubMed based on a query. Returns structured JSON."

    def __call__(self, query: str) -> List[Dict]:
        client = PubMedClient()
        ids = client.search(query=query)
        return client.fetch_details(ids)

    def _run(self, query: str):
        return self.__call__(query)

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported for PubMedTool.")
