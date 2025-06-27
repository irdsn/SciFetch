##################################################################################################
#                                        FASTAPI ENTRYPOINT                                      #
#                                                                                                #
# This FastAPI application exposes an endpoint to run the SciFetch agent, which autonomously     #
# searches and summarizes scientific literature using academic APIs and a user-provided prompt.  #
#                                                                                                #
# Endpoint:                                                                                      #
#   - /run (POST): Executes the agent using a custom prompt and an OpenAI API key.               #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agents.scientific_fetcher import run_agent
from utils.config import OUTPUT_DIR


##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

logging.basicConfig(level=logging.INFO)

##################################################################################################
#                                     FASTAPI INITIALIZATION                                     #
##################################################################################################

app = FastAPI(
    title="SciFetch API",
    description="SciFetch is an autonomous LangChain-based agent designed to search, summarize, "
                "and store scientific literature based on user-provided prompts. "
                "It intelligently selects the best academic APIs for each topic, "
                "provides a synthesized summary, and outputs results in Markdown.",
    version="1.0.0"
)

##################################################################################################
#                                         REQUEST MODEL                                          #
##################################################################################################

class PromptRequest(BaseModel):
    """
    Request schema for the /run endpoint.
    Requires a natural language prompt and an OpenAI API key.
    """
    prompt: str
    api_key: str

##################################################################################################
#                                           ENDPOINTS                                            #
##################################################################################################

@app.post("/run")
def run_scifetch(request: PromptRequest):
    """
    Executes the SciFetch agent using the provided prompt and API key.

    Args:
        request (PromptRequest): JSON payload containing 'prompt' and 'api_key'.

    Returns:
        dict: Success message, file info, and Markdown content.
    """
    try:
        # Use request-specific OpenAI API key (does not persist globally)
        os.environ["OPENAI_API_KEY"] = request.api_key

        # Run the autonomous agent
        result = run_agent(request.prompt)

        # Read content to return in response
        with open(result["output_file"], "r", encoding="utf-8") as f:
            content = f.read()

        filename = result["output_file"].split("/")[-1]
        download_url = f"https://scifetch.onrender.com/download/{filename}"

        return {
            "message": "✅ File generated successfully.",
            "filename": filename,
            "download_url": download_url,
            "output_file": result["output_file"],
            "content": content
        }

    except Exception as e:
        logging.exception("❌ Agent execution failed.")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/download/{filename}")
def download_file(filename: str):
    """
    Endpoint to download a generated Markdown report.

    Args:
        filename (str): Name of the file to download (e.g., result.md)

    Returns:
        FileResponse: The file as an attachment to trigger download.
    """
    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="text/markdown",
        filename=filename
    )

##################################################################################################
#                                        ROOT ENDPOINT                                           #
##################################################################################################

@app.get("/")
def read_root():
    """
    Root endpoint to verify API status.

    Returns:
        dict: A welcome message confirming that the API is running.
    """
    return {"message": "SciFetch API is up and running!"}
