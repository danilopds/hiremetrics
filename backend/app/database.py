from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .config import settings
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Configure engine with proper connection pooling and timeout handling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Reduced pool size to avoid overwhelming the database
    max_overflow=10,  # Reduced max overflow
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=1800,  # Recycle connections after 30 minutes (reduced)
    pool_timeout=20,  # Reduced timeout for getting connection from pool
    echo=False,  # Set to True for SQL query logging
    # PostgreSQL specific settings
    connect_args={
        "connect_timeout": 15,  # Increased connection timeout
        "application_name": "saas_jobs_api",  # Application name for monitoring
        "options": "-c timezone=utc -c statement_timeout=30000",  # Set timezone and 30s statement timeout
    },
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # Prevent expired object issues
)

Base = declarative_base()


def get_db():
    """Database dependency with proper connection handling and retry logic"""
    db = SessionLocal()
    try:
        # Test connection before yielding using text()
        db.execute(text("SELECT 1"))
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        db.rollback()
        # Close the connection on error to free up the pool
        try:
            db.close()
        except:
            pass
        raise
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
