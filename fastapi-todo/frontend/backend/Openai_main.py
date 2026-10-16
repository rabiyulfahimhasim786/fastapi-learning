import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load variables from the .env file
load_dotenv()

# Initialize the asynchronous OpenAI client
# It automatically picks up the OPENAI_API_KEY environment variable
openai_client = AsyncOpenAI()

app = FastAPI(
    title="FastAPI OpenAI Integration",
    description="A modern async API endpoint executing OpenAI calls.",
    version="1.0.0"
)

# Define the Pydantic model for request validation
class ChatRequest(BaseModel):
    prompt: str

# Define the Pydantic model for response validation
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Receives a user prompt, makes an asynchronous call to the OpenAI API,
    and returns the generated text response.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API key is missing from environment.")

    try:
        # Non-blocking asynchronous call to OpenAI
        response = await openai_client.responses.create(
            model="gpt-6-astra",
            input=request.prompt
        )
        
        # Extract the text output from the response object
        ai_message = response.output_text
        
        return ChatResponse(response=ai_message)

    except Exception as e:
        # Catch SDK/Network errors and raise a proper HTTP exception
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
