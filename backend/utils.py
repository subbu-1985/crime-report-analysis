#import logging
#from datetime import datetime

#def get_logger(name: str):
 #   """
  #  Returns a configured logger.
   # """
#    logger = logging.getLogger(name)
#    if not logger.handlers:
#        handler = logging.StreamHandler()
#        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
#        handler.setFormatter(formatter)
#       logger.addHandler(handler)
#   logger.setLevel(logging.INFO)
#    return logger

#def parse_iso_datetime(dt_str):
#   """
#    Parse ISO formatted datetime string to datetime object.
#    """
#    try:
#        return datetime.fromisoformat(dt_str)
#    except Exception:
#        return None

#def safe_get(d: dict, key: str, default=None):
#    """
#    Safely get a value from a dict.
#    """
#    return d[key] if key in d else default

#def to_camel_case(snake_str):
#    """
#    Convert snake_case string to camelCase.
#    """
#    components = snake_str.split('_')
#
# return components[0] + ''.join(x.title() for x

import pandas as pd
from database import SessionLocal
from models import CrimeReport
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def load_crime_data() -> pd.DataFrame:
    """Load crime data from database"""
    db = SessionLocal()
    try:
        crimes = db.query(
            CrimeReport.id,
            CrimeReport.timestamp,
            CrimeReport.district,
            CrimeReport.latitude,
            CrimeReport.longitude,
            CrimeReport.crime_type,
            CrimeReport.description
        ).limit(5000).all()  # Adjust limit as needed
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'timestamp': c.timestamp,
            'district': c.district,
            'latitude': c.latitude,
            'longitude': c.longitude,
            'crime_type': c.crime_type,
            'description': c.description,
            'population_density': get_population_density(c.district)  # Implement this
        } for c in crimes])
        
        return df
        
    except Exception as e:
        logger.error(f"Data loading error: {str(e)}")
        raise
    finally:
        db.close()

def get_population_density(district: str) -> float:
    """Get population density for a district"""
    # Implement this with your data source
    # Could be from database or external API
    return 1000.0  # Placeholder