"""from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Example model for a crime record
class CrimeRecord(BaseModel):
    id: int
    district: str
    type: str
    location: str
    severity: int
    timestamp: str

# Dummy data for prototype
DUMMY_CRIMES = [
    {"id": 1, "district": "Guntur", "type": "Theft", "location": "Guntur City", "severity": 3, "timestamp": "2025-07-23T10:00:00"},
    {"id": 2, "district": "Vijayawada", "type": "Assault", "location": "Vijayawada Central", "severity": 4, "timestamp": "2025-07-23T09:30:00"},
]

@router.get("/crimes", response_model=List[CrimeRecord])
def get_crimes(district: Optional[str] = Query(None)):
    if district:
        return [c for c in DUMMY_CRIMES if c["district"].lower() == district.lower()]
    return DUMMY_CRIMES

@router.get("/stats")
def get_stats(district: str):
    # Dummy stats
    stats = {
        "district": district,
        "total_crimes": 42,
        "top_types": {"Theft": 20, "Assault": 10, "Burglary": 12},
        "hotspots": [
            {"location": "Guntur City", "count": 8},
            {"location": "Vijayawada Central", "count": 6}
        ]
    }
    return stats"""
    
from fastapi import APIRouter, HTTPException, Depends
from services.crime_analysis import analyze_crime_patterns
from models import CrimeReport
from config import settings
import google.generativeai as genai
import logging

router = APIRouter(prefix="/api/crimes", tags=["Crime Analysis"])
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
crime_model = genai.GenerativeModel('gemini-pro')

@router.post("/report", response_model=CrimeReport)
async def report_crime(report_data: dict):
    """Report a new crime incident with AI analysis"""
    try:
        # Get AI analysis
        prompt = f"""
        Analyze this crime report for Andhra Pradesh police:
        Location: {report_data.get('location', 'Unknown')}
        Type: {report_data.get('crime_type', 'Unknown')}
        Description: {report_data.get('description', 'No details')}
        
        Provide:
        1. Severity score (1-10)
        2. Suggested priority (low/medium/high)
        3. Potential related crimes
        4. Recommended police actions
        """
        
        response = crime_model.generate_content(prompt)
        analysis = response.text
        
        return {
            **report_data,
            "analysis": analysis,
            "status": "reported"
        }
        
    except Exception as e:
        logger.error(f"Crime reporting error: {str(e)}")
        raise HTTPException(status_code=500, detail="Crime reporting failed")

@router.get("/patterns")
async def get_crime_patterns(district: str = None):
    """Get crime patterns with Gemini AI analysis"""
    try:
        patterns = await analyze_crime_patterns(district)
        prompt = f"""
        Analyze these crime patterns for Andhra Pradesh:
        {patterns}
        
        Provide insights on:
        1. Emerging trends
        2. Geographic hotspots
        3. Time patterns
        4. Recommended patrol strategies
        """
        
        response = crime_model.generate_content(prompt)
        return {"patterns": patterns, "ai_analysis": response.text}
        
    except Exception as e:
        logger.error(f"Pattern analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")