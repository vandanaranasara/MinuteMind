# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import datetime
from core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# class Transcript(Base):
#     __tablename__ = "transcripts"
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     transcript_text = Column(Text)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)

# def init_db():
#     Base.metadata.create_all(bind=engine)
