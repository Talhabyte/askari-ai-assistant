from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import os

import google.generativeai as genai

from app.prompts import SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="Askari AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Gemini setup
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "askari-ai-assistant"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message.lower().strip()

    if not user_message:
        return ChatResponse(reply="Please enter a message.")

    # 🔥 FAKE TOOL LOGIC (VERY IMPORTANT)
    if "branch timing" in user_message:
        return ChatResponse(
            reply="Our branches are open Monday to Friday from 9 AM to 5 PM. Some branches may have extended hours."
        )

    if "open account" in user_message:
        return ChatResponse(
            reply="To open a savings account, you need CNIC, proof of income, and a completed account form. You can apply online or visit a branch."
        )

    if "atm" in user_message:
        return ChatResponse(
            reply="You can locate the nearest ATM using the bank's mobile app or website under ATM locator."
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser: {user_message}",
        )

        reply_text = response.text.strip() if response.text else "No response generated."
        return ChatResponse(reply=reply_text)

    except Exception:
        return ChatResponse(reply="Service temporarily unavailable. Please try again later.")