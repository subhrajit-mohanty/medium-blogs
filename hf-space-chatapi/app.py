import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer
from tinydb import TinyDB
from tinydb import Query
from datetime import datetime
from utils import generate_token

query = Query()
db = TinyDB(".token.json")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

REF_KEY = "F0eeQ419wvoCSPH7KBmsd9OiVkF0W0DxK1XE9T3BlbkFJ0"
model_name = ""

def verify_token(token: str = Depends(oauth2_scheme)):
    expiry = -1
    res = db.get(query.token == token)

    if res:
        expiry = (datetime.strptime(res["expiry_date"], '%Y-%m-%d') - datetime.strptime(res["created_at"], '%Y-%m-%d')).days
    
    if expiry < 0:
        return {"message": "Token is not Valid"}
    
    return token


class ChatInput(BaseModel):
    message: str
    openAI_token: str
    model_name: str


class RefToken(BaseModel):
    expiry_date: str
    ref_key: str

@app.get("/")
async def base_url():
    try:
        return {
            "Please Check the documentation here": "https://huggingface.co/spaces/Subhraj07/chatapi/blob/main/README.md",
            "Swagger UI" : "https://subhraj07-chatapi.hf.space/docs"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request." + str(e))

@app.post("/create")
async def create(data: RefToken):
    token = "Reference Key is incorrect"
    try:
        if data.ref_key == REF_KEY:
            token = generate_token(data.expiry_date, db) 
            return {"TOKEN": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request." + str(e))

@app.get("/list")
async def list(token: str = Depends(verify_token)):
    try:
        data = db.all()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request." + str(e))

@app.post("/chat")
async def chat(chat_input: ChatInput, token: str = Depends(verify_token)):
    openai.api_key = chat_input.openAI_token
    prompt = f"User: {chat_input.message}\nAI:"
    model_name = chat_input.model_name
    try:
        if model_name == "text-davinci-002":
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.7,
            )
            message = response.choices[0].text.strip()
            usages = response["usage"]
        
        if model_name == "gpt-3.5-turbo":
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   
            messages=[         
                {"role": "system", "content": prompt}   
            ])

            message = response.choices[0]["message"]["content"]
            usages = response["usage"]

        if model_name == "":
            message = "Plase select the model"
            usages = ""

        return {
            "message": message,
            "usages" : usages
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request." + str(e))
