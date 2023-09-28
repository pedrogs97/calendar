"""Service database"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def get_db_session():
    """Returns db session"""
    return Session()