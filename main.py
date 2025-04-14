from typing import Union, Optional
from sqlalchemy import Table, Column, Integer, String

from enum import Enum
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
import models

import json
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# updates
# do the entire tutorial over but every single step from the video (if that doesnt work learn pydantic and JSON feature)

# observation: films refers to the table in the tutorial, but its called bros

# dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_db():
    db = SessionLocal()
    num_gyms = db.query(Gym).count()
    if num_files == 0:
        files = [
            {'name': 'Planet Fitness'},
            {'name': 'Planet Freakness'},
        ]
        for gym in gyms:
            db.add(models.Gym(**film))
        db.commit()
    else:
        print(f"{num_gyms} gyms already in DB")

@app.get("/index/", response_class=HTMLResponse)
async def gymlist(
    request: Request,
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)

):
    gyms = db.query(models.Gym).all()
    print(gyms)

class UserLocation(BaseModel):
    latitude: float
    longitude: float

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/location/")
async def create_location(location: UserLocation):
    
    return {"received_latitude": location.latitude, "received_longitude": location.longitude}