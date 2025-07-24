#def get_heatmap_points(crimes, district=None):
 #   """
  #  Return geo-coordinates and severity for crimes in a district.
   # """
    # Example: crimes should have 'lat', 'lng', 'severity'
    #if district:
     #   crimes = [c for c in crimes if c["district"].lower() == district.lower()]
    #points = []
    #for c in crimes:
     #   if "lat" in c and "lng" in c:
      #      points.append({
       #         "lat": c["lat"],
        #        "lng": c["lng"],
         #       "severity": c.get("severity", 1)
          #  })
    #return points
    
from models import District, CrimeReport
from database import SessionLocal
from typing import Dict, Optional
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

async def get_district_geodata(district_name: str) -> Dict:
    """Get geographic data for a specific district"""
    db = SessionLocal()
    try:
        # Check if district exists in database
        district = db.query(District).filter(
            District.name == district_name).first()
            
        if not district:
            # Fallback to JSON data
            return await get_district_from_json(district_name)
            
        # Get recent crimes in this district
        crimes = db.query(CrimeReport).filter(
            CrimeReport.district == district_name,
            CrimeReport.status == "reported"
        ).limit(100).all()
        
        return {
            "district": district.name,
            "coordinates": (district.latitude, district.longitude),
            "boundaries": json.loads(district.boundary_geojson),
            "recent_crimes": [c.serialize() for c in crimes],
            "population": district.population
        }
        
    except Exception as e:
        logger.error(f"Map data error for {district_name}: {str(e)}")
        raise
    finally:
        db.close()

async def get_district_from_json(district_name: str) -> Dict:
    """Fallback to load district data from JSON file"""
    try:
        json_path = Path(__file__).parent.parent.parent / "frontend/data/ap_districts.json"
        with open(json_path) as f:
            data = json.load(f)
            
        district = next((d for d in data["districts"] 
                       if d["name"].lower() == district_name.lower()), None)
        
        if not district:
            raise ValueError(f"District {district_name} not found")
            
        return {
            "district": district["name"],
            "coordinates": (district["lat"], district["lng"]),
            "crime_rate": district["crime_rate"],
            "hotspots": district["hotspots"]
        }
        
    except Exception as e:
        logger.error(f"JSON data load error: {str(e)}")
        raise ValueError(f"Could not load data for {district_name}")