"""from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Crime(Base):
    __tablename__ = "crimes"
    id = Column(Integer, primary_key=True, index=True)
    district = Column(String, index=True)
    type = Column(String, index=True)
    location = Column(String)
    severity = Column(Integer)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    timestamp = Column(DateTime)

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    crime_rate = Column(Float)
    hotspots = Column(Integer)
    last_updated = Column(String)
    population = Column(Integer)
    safety_score = Column(Float)
    crime_trend = Column(String)"""
    
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Sequence
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TSVECTOR
from database import Base
import uuid

class CrimeReport(Base):
    __tablename__ = "crime_reports"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True
    )
    timestamp = Column(DateTime(timezone=True), nullable=False)
    district = Column(String(50), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    crime_type = Column(String(50), index=True, nullable=False)  # e.g., "theft", "assault"
    description = Column(Text)
    status = Column(String(20), default="reported", index=True)
    severity = Column(Integer, default=1)  # 1-10 scale
    officer_notes = Column(JSON)
    tags = Column(ARRAY(String))  # For categorizing reports
    
    # Full text search capability
    search_vector = Column(TSVECTOR)

class CrimePattern(Base):
    __tablename__ = "crime_patterns"
    
    id = Column(
        Integer,
        Sequence('crime_pattern_id_seq'),
        primary_key=True,
        index=True
    )
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    district = Column(String(50), index=True, nullable=False)
    crime_type = Column(String(50), index=True, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    trend = Column(String(20))  # 'increasing', 'decreasing', 'stable'
    hotspot_coordinates = Column(ARRAY(Float))  # [lat, lng] pairs
    time_distribution = Column(JSON)  # Hourly/daily distribution
    
    __table_args__ = (
        {'postgresql_partition_by': 'RANGE (date)'},  # For time-series partitioning
    )

class District(Base):
    __tablename__ = "districts"
    
    id = Column(
        Integer,
        Sequence('district_id_seq'),
        primary_key=True,
        index=True
    )
    name = Column(String(50), unique=True, nullable=False)
    code = Column(String(10), unique=True)  # Short district code
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    boundary_geojson = Column(JSON, nullable=False)
    population = Column(Integer)
    density = Column(Float)  # persons per sq km
    police_stations = Column(Integer)
    crime_rate = Column(Float)  # crimes per 1000 population
    last_updated = Column(DateTime(timezone=True))
    
    # Spatial index would be created separately
    # CREATE INDEX idx_districts_geom ON districts USING GIST (ST_GeomFromGeoJSON(boundary_geojson));

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(
        Integer,
        Sequence('faq_id_seq'),
        primary_key=True,
        index=True
    )
    question = Column(Text, unique=True, nullable=False)
    answer = Column(Text, nullable=False)
    language = Column(String(10), default="en", index=True)
    category = Column(String(50), index=True)
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow)
    popularity = Column(Integer, default=0)  # Track frequently asked questions
    keywords = Column(ARRAY(String))  # For better search
    
    # Full text search capability
    search_vector = Column(TSVECTOR)