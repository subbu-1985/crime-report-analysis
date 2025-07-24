"""import requests
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

GEMINI_API_KEY = "AIzaSyAvxl_BuYekKIh5QllE6mGV2F0au_FIAtM"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

class ChatRequest(BaseModel):
    message: str

@router.post("/chatbot")
def chatbot(req: ChatRequest):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": req.message}]}
        ]
    }
    params = {"key": GEMINI_API_KEY}
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            reply = "Sorry, I couldn't process your request."
        return {"reply": reply}
    else:
        return {"reply": "Sorry, Gemini API error."}"""

from fastapi import APIRouter, HTTPException, Request
from config import settings
import google.generativeai as genai
import logging
from typing import Dict

router = APIRouter(prefix="/api/chatbot", tags=["Police Assistant"])
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
chatbot_model = genai.GenerativeModel('gemini-pro')

# Chat history storage
chat_sessions: Dict[str, any] = {}

@router.post("/query")
async def handle_chat_query(request: Request):
    """Handle chatbot queries with Gemini"""
    try:
        data = await request.json()
        session_id = data.get("session_id", "default")
        message = data["message"]
        
        # Get or create chat session
        if session_id not in chat_sessions:
            chat = chatbot_model.start_chat(history=[])
            chat_sessions[session_id] = chat
        else:
            chat = chat_sessions[session_id]
        
        # AP Police specific context
        context = """
        You are an AI assistant for Andhra Pradesh Police. Your responses should:
        1. Be concise and factual
        2. Focus on crime prevention and safety
        3. Provide official contacts when needed
        4. Use simple English and Telugu terms
        5. Direct to human officers for sensitive matters
        """
        
        full_prompt = f"{context}\nUser: {message}"
        
        # Get response
        response = chat.send_message(full_prompt)
        
        return {
            "response": response.text,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Chatbot service unavailable. Please try again later."
        )

@router.get("/emergency-contacts")
async def get_emergency_contacts():
    """Get AP-specific emergency contacts with AI explanation"""
    try:
        prompt = """
        List emergency contacts for Andhra Pradesh Police with brief descriptions in English and Telugu.
        Format as:
        1. Contact Name - Number - Purpose (English/Telugu)
        """
        
        response = chatbot_model.generate_content(prompt)
        return {"contacts": response.text}
        
    except Exception as e:
        logger.error(f"Contacts error: {str(e)}")
        return {
            "contacts": [
                "Emergency: 100",
                "Women Safety: 181",
                "Cyber Crime: 155620"
            ]
        }