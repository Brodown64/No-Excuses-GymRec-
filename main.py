from fastapi import FastAPI, Request, Header, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from folium import Map


import os
import json
import pathlib
import geopandas as gpd 
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

ox.__version__

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

# updates
# idfk man figure out folium
# use http://localhost:8000 from now on

class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

# user = User(name="dick", email="mutasimhussein1@gmail.com", account_id=1234)

json_str = pathlib.Path("user.json").read_text()
user = User.model_validate_json(json_str)

print(user.name)
print(user.email)
print(user.account_id)

# AOI = 'Minneapolis, Minnesota, USA'
# aoi_gdf = ox.geocode_to_gdf(AOI)

# # area of interest plotted 
# basemap = aoi_gdf.explore(color='lightblue')
# basemap

#interactive code
m.save('map.html')

#interactive code (end)

class UserLocation(BaseModel):
    latitude: float
    longitude: float

# @app.get("/")
# async def root(request: Request, db: Session = Depends(get_db)):
#     gyms = crud.get_gyms(db)
#     return templates.TemplateResponse("index.html", {"request": request, "gyms": gyms})
#     return {"message": "Hello World"}

@app.get("/", response_class=HTMLResponse)
async def root():
    m = Map()
    return m.get_root().render()

@app.post("/gyms/", response_model=schemas.Gym)
def add_gym(gym: schemas.GymCreate, db: Session = Depends(get_db)):
    return crud.create_gym(db, gym)

@app.get("/gyms/", response_model=list[schemas.Gym])
def list_gyms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_gyms(db, skip=skip, limit=limit)

