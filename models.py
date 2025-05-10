from sqlalchemy import Table, Column, Integer, String, Float

from database import Base 

class User(Base):
    __tablename__ = "bros"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    age = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer, primary_key=True, index=True)
    ratings = Column(Integer, primary_key=True, index=True)

class Gym(Base):
    __tablename__ = "gyms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
# models created from SQLAlchemy

