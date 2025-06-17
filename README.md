# SciFetch: Autonomous Agent for Scientific Literature Retrieval

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![AI](https://img.shields.io/badge/AI-LangChain-blueviolet)
![Task](https://img.shields.io/badge/Task-Information_Retrieval-orange)
![Last Updated](https://img.shields.io/badge/Last%20Updated-May%202025-brightgreen)

SciFetch is an autonomous LangChain-based agent designed to search, summarize, and store scientific literature based on user-provided prompts. It intelligently selects the best academic APIs for each topic, provides a synthesized summary, and outputs results in Markdown.

---

## Author

Íñigo Rodríguez Sánchez  
Data & Artificial Intelligence Engineer

---

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Script Overview](#script-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Future Work](#future-work)
- [Final Words](#final-words)

---

## Introduction

**SciFetch** is a Python-based autonomous agent designed to assist researchers in quickly gathering and synthesizing scientific literature.

The project originated from real-world needs to automate topic exploration, reduce manual article screening, and centralize findings in well-formatted outputs.  

It leverages the power of large language models (GPT-4o), planning agents (LangChain), and multiple academic APIs to retrieve high-quality scientific content.

SciFetch aims to provide:

- Fast and structured access to academic knowledge
- Summarized, readable overviews of complex topics
- A foundation for building research tools, assistants, or pipelines
- Reliability ensured through unit and integration tests with 89% code coverage

> Note: SciFetch currently runs locally and is not yet deployed as a public web service.

---

## Key Features

- **Multi-source Scientific Retrieval:** Queries across PubMed, arXiv, OpenAlex, EuropePMC, and CrossRef.
- **LangChain Autonomous Agent:** Uses a ReAct-style planner to dynamically select the best tools based on the input prompt.
- **LLM-Powered Summarization:** Synthesizes results into a coherent, human-readable overview using GPT-4o.
- **Markdown Output Generation:** Exports findings to `.md` files, including summaries and lists of relevant articles.
- **Graceful Failure Handling:** Logs errors when a specific API fails but continues processing with other sources.
- **API-Key Secured:** Requires only an OpenAI API key in a `.env` file to run.
- **Internet-Connected Runtime:** Works with real-time API calls to ensure up-to-date academic content.
- **Tested for Reliability:** Includes unit and integration tests with 89% coverage to ensure robustness.

---

## Project Structure

```bash
SciFetch/
├── agents/                    # Core agent logic
│   └── scientific_fetcher.py  # Main autonomous agent that orchestrates API tools
│
├── apis/                      # Scientific API integrations
│   ├── arXiv.py               # arXiv search client and LangChain tool
│   ├── CrossRef.py            # CrossRef metadata retriever
│   ├── EuropePMC.py           # Europe PMC API wrapper
│   ├── OpenAlex.py            # OpenAlex client with inverted abstract decoding
│   └── PubMed.py              # PubMed search and fetch logic
│
├── inputs/                    
│   └── prompts.txt            # Input prompts for test runs
│
├── outputs/                   # Generated summaries in Markdown format
│   └── input_prompt.md        # Example output file (one per input prompt)
│
├── tests/                     # Pytest test suite (unit + integration)
│   ├── test_app.py
│   ├── test_arxiv.py
│   ├── test_crossref.py
│   ├── test_europepmc.py
│   ├── test_openalex.py
│   ├── test_pubmed.py
│   └── test_scientific_fetcher.py
│
├── utils/                     # Utilities and configuration
│   └── logs_config.py         # Color-coded logging setup
│
├── .env.example               # Template for environment variables
├── .gitignore                 # Files and folders to ignore in Git
├── app.py                     # FastAPI entrypoint for running the agent via HTTP
├── pytest.ini                 # Pytest configuration (warnings, env setup, etc.)
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

---

## Script Overview

| Script / Module                | Description                                                                                                                                  |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `agents/scientific_fetcher.py` | Main agent script that takes a user prompt, queries academic APIs, summarizes findings using GPT-4o, and saves the output to Markdown.       |
| `apis/arXiv.py`                | Interface for querying the arXiv API and extracting metadata. Includes LangChain-compatible tool wrapper.                                    |
| `apis/CrossRef.py`             | Retrieves publication metadata from CrossRef. Cleans and filters fields like DOI, title, abstract, and date.                                 |
| `apis/EuropePMC.py`            | Connects to the Europe PMC API and returns structured article metadata. LangChain-ready.                                                     |
| `apis/OpenAlex.py`             | Queries OpenAlex API and decodes abstracts from inverted index format. Provides unified metadata output.                                     |
| `apis/PubMed.py`               | Uses PubMed's E-utilities to search and fetch publication metadata. Parses XML response into structured JSON.                                |
| `utils/logs_config.py`         | Centralized logging configuration with color-coded output for different log levels.                                                          |

---

## Tests & Coverage

![Coverage](https://img.shields.io/badge/Coverage-89%25-brightgreen)
![Tested](https://img.shields.io/badge/Tested-Pytest-blue)

SciFetch includes a robust test suite to ensure stability, API correctness, and agent reliability across its components.

All core modules and external API clients are covered by unit and integration tests using `pytest` and `pytest-cov`.

| Test File                          | Description                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
| `tests/test_app.py`                | Tests the FastAPI /run endpoint with a mocked run_agent.                    |
| `tests/test_arxiv.py`              | Verifies that ArxivClient and ArxivTool return valid responses.             |
| `tests/test_crossref.py`           | Tests CrossRefClient's date extraction, abstract cleaning, and tool output. |
| `tests/test_europepmc.py`          | Checks metadata extraction from EuropePMC API via client and tool.          |
| `tests/test_openalex.py`           | Tests abstract decoding logic and tool results for OpenAlex.                |
| `tests/test_pubmed.py`             | Validates PubMed ID search, metadata parsing, and tool integration.         |
| `tests/test_scientific_fetcher.py` | Covers run_agent() integration and article relevance extraction logic.      |


Once the full suite is executed, the following results were obtained from the latest full test run on the main branch:

```bash
python -m pytest --cov=agents --cov=app --cov=apis tests/

<details>
======================================================= test session starts ========================================================
platform darwin -- Python 3.11.10, pytest-8.4.0, pluggy-1.6.0
plugins: anyio-4.9.0, cov-6.2.1, langsmith-0.3.38
collected 20 items                                                                                                                 

tests/test_app.py .                                                                                                          [  5%]
tests/test_arxiv.py ....                                                                                                     [ 25%]
tests/test_crossref.py ....                                                                                                  [ 45%]
tests/test_europepmc.py ...                                                                                                  [ 60%]
tests/test_openalex.py ...                                                                                                   [ 75%]
tests/test_pubmed.py ...                                                                                                     [ 90%]
tests/test_scientific_fetcher.py ..                                                                                          [100%]

========================================================== tests coverage ==========================================================
Name                           Stmts   Miss  Cover
--------------------------------------------------
agents/scientific_fetcher.py      64     10    84%
apis/CrossRef.py                  51      4    92%
apis/EuropePMC.py                 22      2    91%
apis/OpenAlex.py                  26      1    96%
apis/PubMed.py                    66      9    86%
apis/arXiv.py                     30      1    97%
app.py                            20      3    85%
--------------------------------------------------
TOTAL                            279     30    89%
</details>
```

These tests give confidence that core modules behave reliably under various scenarios and inputs. High coverage ensures robustness across future updates.

---

## Installation

To run SciFetch locally, follow these steps:

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/SciFetch.git
cd SciFetch
```

2. (Optional but recommended) Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

4. Add your OpenAI key on the .env file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

> Note: The application currently runs locally only and is not deployed as a public API or web service.

---

## Usage

You can use SciFetch in **two ways**, depending on whether you want an interactive console or a local API.

### Option 1: Run the agent via CLI (recommended for exploration)

Launch the agent script and enter your prompt interactively:

```bash
python agents/scientific_fetcher.py
```

Then enter your prompt interactively, e.g.:

```
Provide your scientific research prompt:
Applications of self-supervised learning in genomics
```

Generated outputs will be saved to the `downloads/SciFetch` folder as a `.md` file.

### Option 2: Run the FastAPI server locally

You can expose the agent functionality via a local REST API:
```bash
uvicorn app:app --reload
```

Then access the interactive documentation at:
```bash
http://127.0.0.1:8000/docs
```

The /run endpoint expects a POST request with the following JSON body:
```json
{
  "prompt": "Applications of self-supervised learning in genomics",
  "api_key": "your_openai_api_key_here"
}
```

The server will return:
```json
{
  "message": "✅ File generated successfully.",
  "output_file": "/Users/user/Downloads/SciFetch/applications_of_self-supervised_learning_in_genomics.md"
}
```

The OpenAI API key is required for every request, even if already present in the .env file.

---

## Future Work

Although SciFetch is functional and production-ready, there are multiple directions for future enhancements:

- **LLM Self-Evaluation:** Score or rank article relevance based on confidence or alignment with the prompt.
- **PDF Exporting Support:** Add native `.pdf` export alongside Markdown.
- **API Usage Monitoring:** Track rate limits, quota consumption, and retries per tool.
- **Multilingual Summarization:** Enable output generation in multiple languages.
- **Tool Expansion:** Include additional APIs like Semantic Scholar, CORE, or IEEE Xplore.
- **Web Interface:** Provide a lightweight web app (e.g., Streamlit) for broader accessibility.
- **Offline LLM Compatibility:** Explore integration with open-source models (e.g., LLaMA or Mistral) for offline use.
- **Public Deployment Option:** Explore hosting the FastAPI backend on platforms to make SciFetch publicly accessible.

---

## Final Words

SciFetch is a small but ambitious project, built to help researchers and engineers accelerate the information gathering process.   
It is an evolving tool, open for experimentation, extension, or integration into larger pipelines or interfaces.

Feel free to explore, extend, or integrate it into your own applications. Contributions, feedback, or improvements are always welcome.

**If you’ve found this project useful or inspiring — feel free to build on it, break it, or just drop a star 🌟.**

