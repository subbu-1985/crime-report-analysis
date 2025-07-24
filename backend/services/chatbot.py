#import requests

#def ask_gemini(message, api_key):
 #   """
  #  Send a message to Gemini API and return the reply.
   # """
    #url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    #headers = {"Content-Type": "application/json"}
    #data = {
     #   "contents": [
      #      {"parts": [{"text": message}]}
       # ]
    #}
    #params = {"key": api_key}
    #response = requests.post(url, headers=headers, params=params, json=data)
    #if response.status_code == 200:
     #   result = response.json()
      #  try:
     #       reply = result["candidates"][0]["content"]["parts"][0]["text"]
      #  except Exception:
       ##     reply = "Sorry, I couldn't process your request."
        #return reply
    #else:
     #   return "Sorry, Gemini API error."
     
from typing import Dict, List
import logging
from config import settings
import google.generativeai as genai
from models import FAQ
from database import SessionLocal

logger = logging.getLogger(__name__)

# Initialize Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ChatbotService:
    def __init__(self):
        self.sessions: Dict[str, any] = {}
        self.faqs = self.load_faqs()

    def load_faqs(self) -> List[Dict]:
        """Load frequently asked questions from database"""
        db = SessionLocal()
        try:
            return [
                {"question": faq.question, "answer": faq.answer}
                for faq in db.query(FAQ).all()
            ]
        except Exception as e:
            logger.error(f"FAQ load error: {str(e)}")
            return []
        finally:
            db.close()

    async def get_response(self, session_id: str, message: str) -> str:
        """Get chatbot response with context"""
        try:
            # Check if we have a matching FAQ first
            faq_response = self.check_faqs(message)
            if faq_response:
                return faq_response

            # Get or create chat session
            if session_id not in self.sessions:
                self.sessions[session_id] = model.start_chat(history=[])
            
            chat = self.sessions[session_id]
            
            # Add AP Police context
            context = """
            You are an assistant for Andhra Pradesh Police. Follow these rules:
            1. Respond in English or Telugu based on user's language
            2. For emergencies, always say "Call 100 immediately"
            3. Be factual and official
            4. Keep responses under 3 sentences unless details requested
            5. For complex queries, suggest visiting nearest police station
            """
            
            response = chat.send_message(f"{context}\nUser: {message}")
            return response.text
            
        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}")
            return "I'm unable to respond now. Please call 100 for emergencies or try again later."

    def check_faqs(self, message: str) -> Optional[str]:
        """Check if question matches any FAQs"""
        message_lower = message.lower()
        for faq in self.faqs:
            if faq["question"].lower() in message_lower:
                return faq["answer"]
        return None

    def get_emergency_contacts(self) -> List[Dict]:
        """Get standard emergency contacts"""
        return [
            {"name": "Emergency", "number": "100", "description": "Police/Fire/Ambulance"},
            {"name": "Women Safety", "number": "181", "description": "Disha Women Helpline"},
            {"name": "Cyber Crime", "number": "155620", "description": "Cyber Crime Complaints"},
            {"name": "Child Helpline", "number": "1098", "description": "Child in Danger"}
        ]