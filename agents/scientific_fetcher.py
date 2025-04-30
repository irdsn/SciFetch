##################################################################################################
#                                        SCIENTIFIC FETCHER                                     #
#                                                                                                #
# Autonomous LangChain Agent that chooses the best scientific APIs (tools) to fetch academic     #
# papers based on a user-defined research prompt. It returns both raw article data and a summary #
# analysis with top relevant articles, and saves the output in Markdown format.                  #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any

from apis.PubMed import PubMedTool
from apis.arXiv import ArxivTool
from apis.OpenAlex import OpenAlexTool
from apis.EuropePMC import EuropePMCTool
from apis.CrossRef import CrossRefTool
from utils.logs_config import logger

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
##################################################################################################
#                                EXECUTE SCIENTIFIC FETCHING AGENT                              #
##################################################################################################

def extract_relevant_articles(summary: str, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    matched_titles = []
    for article in articles:
        title = article.get("title", "").lower()
        for line in summary.split("\n"):
            if title and title in line.lower():
                matched_titles.append(article)
                break
    return matched_titles

def run_scientific_fetcher(prompt: str) -> Dict[str, Any]:
    tools = [
        Tool(name=tool.name, func=tool(), description=tool.description)
        for tool in [ArxivTool, PubMedTool, OpenAlexTool, EuropePMCTool, CrossRefTool]
    ]

    llm = ChatOpenAI(temperature=0.2, model="gpt-4o")

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        return_intermediate_steps=True
    )

    logger.info("\U0001F680 Launching autonomous agent for scientific literature fetching...")

    try:
        result = agent.invoke({"input": prompt})
        intermediate_steps = result.get("intermediate_steps", [])

        articles = []
        for step in intermediate_steps:
            if (
                isinstance(step, tuple)
                and isinstance(step[1], list)
                and all(isinstance(item, dict) for item in step[1])
            ):
                articles.extend(step[1])

        summary_prompt = (
            "You are a scientific assistant. Based on the user's query: \n"
            f"'{prompt}'\n"
            "And the following articles found (titles and abstracts), write a short summary of the topic, "
            "highlighting the most relevant papers and their contributions. Use at least 5 papers if they are sufficiently related.\n\n"
        )

        for article in articles:
            summary_prompt += f"- {article.get('title', '')}: {article.get('abstract', '')[:500]}\n"

        summary_response = llm.invoke(summary_prompt)
        summary = summary_response.content.strip()

        logger.info("✅ Agent completed run.")

        relevant_articles = extract_relevant_articles(summary, articles)
        for article in relevant_articles:
            title = article.get("title", "")
            if title:
                summary = summary.replace(title, f"**{title}**")

        markdown_output = f"# Scientific Summary\n\n**Prompt:** {prompt}\n\n**Summary:**\n{summary}\n\n---\n\n## Information on the total number of items extracted, including those identified as most relevant by the agent ({len(articles)})\n"

        for idx, article in enumerate(articles, 1):
            markdown_output += (
                f"\n### {idx}. {article.get('title', 'No Title')}\n"
                f"- **Date:** {article.get('publication_date', 'Unknown')}\n"
                f"- **Source:** {article.get('source', 'Unknown')}\n"
                f"- **URL:** [{article.get('url')}]({article.get('url')})\n"
                + (f"- **DOI:** {article['doi']}\n" if article.get("doi") else "") +
                f"- **Abstract:** {article.get('abstract', '')[:500]}...\n"
            )

        filename = prompt.lower().strip().replace(" ", "_").replace("/", "_")
        output_path = OUTPUT_DIR / f"{filename}.md"
        output_path.write_text(markdown_output, encoding="utf-8")

        result_data = {
            "summary": summary,
            "articles": articles,
            "markdown": markdown_output,
            "output_file": str(output_path)
        }

        return result_data

    except Exception as e:
        logger.error(f"❌ Agent failed with error: {e}")
        return {"summary": "", "articles": [], "markdown": "", "output_file": ""}

##################################################################################################
#                                          TEST MAIN                                             #
##################################################################################################

if __name__ == "__main__":
    user_prompt = input("Enter your scientific research prompt: ")
    result = run_scientific_fetcher(user_prompt)
    print(result["markdown"])
    print(f"\n✅ Output saved to: {result['output_file']}")
