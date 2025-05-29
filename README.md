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

---

## Key Features

- **Multi-source Scientific Retrieval:** Queries across PubMed, arXiv, OpenAlex, EuropePMC, and CrossRef.
- **LangChain Autonomous Agent:** Uses a ReAct-style planner to dynamically select the best tools based on the input prompt.
- **LLM-Powered Summarization:** Synthesizes results into a coherent, human-readable overview using GPT-4o.
- **Markdown Output Generation:** Exports findings to `.md` files, including summaries and lists of relevant articles.
- **Graceful Failure Handling:** Logs errors when a specific API fails but continues processing with other sources.
- **API-Key Secured:** Requires only an OpenAI API key in a `.env` file to run.
- **Internet-Connected Runtime:** Works with real-time API calls to ensure up-to-date academic content.

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
├── utils/                     # Utilities and configuration
│   └── logs_config.py         # Color-coded logging setup
│
├── requirements.txt           # Python dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Files and folders to ignore in Git
└── README.md                  # Project documentation
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

## Installation

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

---

## Usage

To launch the agent, run the script and provide a scientific prompt when requested.

```bash
python agents/scientific_fetcher.py
```

Then enter your prompt interactively, e.g.:

```
Enter your scientific research prompt:
Applications of federated learning in privacy-preserving medical image analysis
```

Generated outputs will be saved to the `outputs/` folder as `.md`.

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

---

## Final Words

SciFetch is a small but ambitious project, built to help researchers and engineers accelerate the information gathering process.   
It is an evolving tool, open for experimentation, extension, or integration into larger pipelines or interfaces.

Feel free to explore, extend, or integrate it into your own applications. Contributions, feedback, or improvements are always welcome.

**If you’ve found this project useful or inspiring — feel free to build on it, break it, or just drop a star 🌟.**

