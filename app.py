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
from fastapi.middleware.cors import CORSMiddleware
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
                "provides a synthesized summary, and outputs results in PDF.",
    version="1.0.0"
)

##################################################################################################
#                                             CORS                                               #
##################################################################################################

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        dict: Success message, file info, HTML preview for frontend, and download link for PDF.
    """
    try:
        # Use request-specific OpenAI API key (does not persist globally)
        os.environ["OPENAI_API_KEY"] = request.api_key

        # Run the autonomous agent
        result = run_agent(request.prompt)

        logging.info(f"Agent result: {result}")

        output_path = result.get("output_file")

        if not output_path:
            raise HTTPException(status_code=500, detail="No output file path returned by agent.")

        # Convert to string path in case it's a Path object
        output_path = str(output_path)


        '''
        # Read content to return in response
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        filename = result["output_file"].split("/")[-1]
        download_url = f"https://scifetch.onrender.com/download/{filename}"

        base_url = os.getenv("BASE_URL", "http://localhost:8000")

        return {
            "message": "✅ File generated successfully.",
            "filename": filename,
            "preview_url": f"{base_url}/preview/{filename}",
            "download_url": f"{base_url}/download/{filename}",
            "output_file": result["output_file"],
            "content": content
        }'''

        filename = os.path.basename(output_path)
        base_url = os.getenv("BASE_URL", "http://localhost:8000")

        return {
            "message": "✅ PDF report generated successfully.",
            "filename": filename,
            "html_preview": result.get("html_preview"),
            "download_url": f"{base_url}/download/{filename}",
            "output_file": output_path
        }

    except Exception as e:
        logging.exception("❌ Agent execution failed.")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/download/{filename}")
def download_file(filename: str):
    """
    Endpoint to download the generated report.

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
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
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
