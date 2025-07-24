"""from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/heatmap")
def get_heatmap(district: str):
    # Dummy geo-coordinates for heatmap
    points = [
        {"lat": 16.3067, "lng": 80.4365, "severity": 3},  # Guntur
        {"lat": 16.5062, "lng": 80.6480, "severity": 4},  # Vijayawada
    ]
    return {"district": district, "points": points}"""
    
from fastapi import APIRouter, HTTPException
from services.map_integration import get_district_geodata
import google.generativeai as genai
from config import settings
import logging

router = APIRouter(prefix="/api/maps", tags=["Map Data"])
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
map_model = genai.GenerativeModel('gemini-pro')

@router.get("/district/{district_name}")
async def get_district_map_data(district_name: str):
    """Get map data with AI-generated insights for a district"""
    try:
        geodata = await get_district_geodata(district_name)
        
        # Get AI insights
        prompt = f"""
        Analyze this geographic data for {district_name} district in Andhra Pradesh:
        {geodata}
        
        Provide:
        1. Crime hotspot identification
        2. Patrol route suggestions
        3. Vulnerable areas
        4. Infrastructure recommendations
        """
        
        response = map_model.generate_content(prompt)
        
        return {
            **geodata,
            "ai_insights": response.text
        }
        
    except Exception as e:
        logger.error(f"Map data error for {district_name}: {str(e)}")
        raise HTTPException(status_code=404, detail="District not found")

@router.get("/hotspots")
async def get_crime_hotspots(radius_km: int = 5):
    """Get crime hotspots with AI analysis"""
    try:
        prompt = f"""
        Generate analysis for crime hotspots in Andhra Pradesh with {radius_km}km radius.
        Consider:
        1. Urban vs rural patterns
        2. Temporal trends
        3. Crime type clusters
        4. Recommended police deployment
        """
        
        response = map_model.generate_content(prompt)
        return {"analysis": response.text}
        
    except Exception as e:
        logger.error(f"Hotspot analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Hotspot analysis failed")