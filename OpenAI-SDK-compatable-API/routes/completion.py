from fastapi import APIRouter, HTTPException, Depends
from routes import ChatCompletionRequest, Message
from starlette.responses import StreamingResponse
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional, List
import asyncio
import time
import json
import os

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_KEY = "1234"  # Replace with your actual API key
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

router = APIRouter()

client = OpenAI(
  api_key = GROQ_API_KEY,
  base_url = BASE_URL
)

def verify_api_key(api_key: str = Depends(api_key_header)):
  if api_key is None:
        print("API key is missing")
        raise HTTPException(status_code=403, detail="API key is missing")
  if api_key != f"Bearer {API_KEY}":
      print(f"Invalid API key: {api_key}")
      raise HTTPException(status_code=403, detail="Could not validate API key")
  print(f"API key validated: {api_key}")

async def _resp_async_generator(messages: List[Message], model: str, max_tokens: int, temperature: float):
   
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": m.role, "content": m.content} for m in messages],
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True
    )

    # Iterate over the response synchronously
    for chunk in response:
        # Convert chunk to serializable format
        chunk_data = chunk.to_dict()
        yield f"data: {json.dumps(chunk_data)}\n\n"
        await asyncio.sleep(0.01)  # Small delay to simulate streaming behavior
    yield "data: [DONE]\n\n"

@router.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatCompletionRequest):

  if request.messages:
        if request.stream:
            return StreamingResponse(
                _resp_async_generator(
                    messages=request.messages,
                    model=request.model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature
                ), media_type="application/x-ndjson"
            )
        else:
            response = client.chat.completions.create(
                model=request.model,
                messages=[{"role": m.role, "content": m.content} for m in request.messages],
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
            return response
  else:
      return HTTPException(status_code=400, detail="No messages provided")