# from sqlalchemy import Column, Integer, String, Text, DateTime
# import datetime
# from backend.database import Base, engine

# class Transcript(Base):
#     __tablename__ = "transcripts"
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     transcript_text = Column(Text)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)

# def init_db():
#     Base.metadata.create_all(bind=engine)