"""from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Create SQLAlchemy engine and session
engine = create_engine(settings.DB_URL, pool_size=settings.DB_POOL_SIZE, max_overflow=settings.DB_MAX_OVERFLOW)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()"""
        
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# Encode password for special characters
encoded_password = quote_plus("Subbu")

# Configure database engine
engine = create_engine(
    f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/ap_crime_db",
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Rest of the db.py file remains the same...

async def init_db():
    """Initialize database with PostGIS extensions and tables"""
    try:
        # Create all tables
        from models import Base
        Base.metadata.create_all(bind=engine)
        
        # Initialize PostgreSQL extensions
        with engine.connect() as conn:
            # Required extensions
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\""))
            conn.execute(text(f"CREATE EXTENSION IF NOT EXISTS \"postgis\" VERSION '{settings.POSTGIS_VERSION}'"))
            
            # Full-text search trigger for FAQs
            conn.execute(text("""
            CREATE OR REPLACE FUNCTION faq_search_vector_update() RETURNS trigger AS $$
            BEGIN
                NEW.search_vector := to_tsvector('english', COALESCE(NEW.question,'') || ' ' || COALESCE(NEW.answer,''));
                RETURN NEW;
            END
            $$ LANGUAGE plpgsql;
            
            DROP TRIGGER IF EXISTS faq_tsvector_update ON faqs;
            CREATE TRIGGER faq_tsvector_update BEFORE INSERT OR UPDATE
            ON faqs FOR EACH ROW EXECUTE FUNCTION faq_search_vector_update();
            """))
            
            # Spatial index for districts
            conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_districts_geom ON districts 
            USING GIST (ST_GeomFromGeoJSON(boundary_geojson));
            """))
            
            conn.commit()
        
        logger.info("PostgreSQL extensions and indexes initialized")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()