#def get_crime_stats(crimes, district=None):
 #   """
  #  Calculate stats for crimes, optionally filtered by district.
   # """
    #if district:
    #   crimes = [c for c in crimes if c["district"].lower() == district.lower()]
    #total = len(crimes)
    #type_counts = {}
    #for c in crimes:
     #   type_counts[c["type"]] = type_counts.get(c["type"], 0) + 1
    #return {
     #   "total_crimes": total,
      #  "top_types": type_counts
    #}

#def find_hotspots(crimes, top_n=3):
 #   """
  #  Find top N locations with most crimes.
   # """
    #loc_counts = {}
    #for c in crimes:
      #  loc_counts[c["location"]] = loc_counts.get(c["location"], 0) + 1
    #sorted_locs = sorted(loc_counts.items(), key=lambda x: x[1], reverse=True)
    #return [{"location": loc, "count": count} for loc, count in sorted_locs[:top_n]]

from models import CrimePattern, CrimeReport
from db import SessionLocal
from typing import Optional, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

async def analyze_crime_patterns(district: Optional[str] = None) -> List[CrimePattern]:
    """Analyze crime patterns for a specific district or statewide"""
    db = SessionLocal()
    try:
        # Base query - last 30 days data
        query = db.query(CrimePattern).filter(
            CrimePattern.date >= datetime.now() - timedelta(days=30)
            
        if district:
            query = query.filter(CrimePattern.district == district)
            
        patterns = query.order_by(CrimePattern.date.desc()).all()
        
        # Generate summary statistics
        if patterns:
            return {
                "total_incidents": len(patterns),
                "crime_types": count_by_type(patterns),
                "hotspots": identify_hotspots(patterns),
                "time_distribution": time_distribution(patterns),
                "district": district or "All Andhra Pradesh"
            }
        return []
        
    except Exception as e:
        logger.error(f"Crime pattern analysis error: {str(e)}")
        raise
    finally:
        db.close()

def count_by_type(patterns: List[CrimePattern]) -> dict:
    """Count crimes by type"""
    type_counts = {}
    for pattern in patterns:
        if pattern.crime_type not in type_counts:
            type_counts[pattern.crime_type] = 0
        type_counts[pattern.crime_type] += 1
    return type_counts

def identify_hotspots(patterns: List[CrimePattern], top_n: int = 3) -> list:
    """Identify top crime hotspots"""
    locations = {}
    for pattern in patterns:
        loc = (pattern.latitude, pattern.longitude)
        if loc not in locations:
            locations[loc] = 0
        locations[loc] += 1
    
    return sorted(locations.items(), key=lambda x: x[1], reverse=True)[:top_n]

def time_distribution(patterns: List[CrimePattern]) -> dict:
    """Analyze crime by time of day"""
    time_slots = {
        "00:00-06:00": 0,
        "06:00-12:00": 0,
        "12:00-18:00": 0,
        "18:00-00:00": 0
    }
    
    for pattern in patterns:
        hour = pattern.timestamp.hour
        if 0 <= hour < 6:
            time_slots["00:00-06:00"] += 1
        elif 6 <= hour < 12:
            time_slots["06:00-12:00"] += 1
        elif 12 <= hour < 18:
            time_slots["12:00-18:00"] += 1
        else:
            time_slots["18:00-00:00"] += 1
            
    return time_slots