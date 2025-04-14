from sqlalchemy import Table, Column, Integer, String

from database import Base 

class Gym(Base):
    __tablename__ = "bros"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    age = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer, primary_key=True, index=True)
    ratings = Column(Integer, primary_key=True, index=True)