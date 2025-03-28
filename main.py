from typing import Union
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine    

from enum import Enum
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
Base = declarative_base()

import json
app = FastAPI()

engine = create_engine("postgresql+psycopg2://postgres:liinaabdi12SQL@localhost:5432/gymdb")

class Gym(Base):
    __tablename__ = "gymdb"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    age = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer, primary_key=True, index=True)
    ratings = Column(Integer, primary_key=True, index=True)

class UserLocation(BaseModel):
    latitude: float
    longitude: float

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/location/")
async def create_location(location: UserLocation):
    
    return {"received_latitude": location.latitude, "received_longitude": location.longitude}