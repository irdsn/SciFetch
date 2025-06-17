from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.scientific_fetcher import run_agent
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="SciFetch API",
    description="SciFetch is an autonomous LangChain-based agent designed to search, summarize, and store scientific literature based on user-provided prompts. It intelligently selects the best academic APIs for each topic, provides a synthesized summary, and outputs results in Markdown.",
    version="1.0.0"
)

class PromptRequest(BaseModel):
    prompt: str
    api_key: str

@app.post("/run")
def run_scifetch(request: PromptRequest):
    """
    Executes the scientific agent using a provided prompt and OpenAI API key.
    """
    try:
        os.environ["OPENAI_API_KEY"] = request.api_key  # Override global key for this request

        result = run_agent(request.prompt)

        return {
            "message": "✅ File generated successfully.",
            "output_file": result["output_file"]
        }

    except Exception as e:
        logging.exception("Agent execution failed")
        raise HTTPException(status_code=500, detail=str(e))
