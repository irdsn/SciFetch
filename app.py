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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.scientific_fetcher import run_agent
import os
import logging

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
        dict: Success message and path to the generated output file.
    """
    try:
        # Use request-specific OpenAI API key (does not persist globally)
        os.environ["OPENAI_API_KEY"] = request.api_key

        # Run the autonomous agent
        result = run_agent(request.prompt)

        return {
            "message": "✅ File generated successfully.",
            "output_file": result["output_file"]
        }

    except Exception as e:
        logging.exception("❌ Agent execution failed.")
        raise HTTPException(status_code=500, detail=str(e))

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
