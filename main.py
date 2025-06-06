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
from map import m
import requests
import folium


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

bbox = [40.70, -74.02, 40.78, -73.95] 

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
# integrate the map with FastAPI site
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
m.save('osm_gyms_map.html')

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

@app.get("/map", response_class=HTMLResponse)
def show_map(request: Request):
    # OSM Overpass Query for gyms and fitness centres
    query = f"""
    [out:json];
    (
      node["amenity"="gym"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      way["amenity"="gym"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      relation["amenity"="gym"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      node["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      way["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      relation["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out center;
    """
    response = requests.post("http://overpass-api.de/api/interpreter", data={"data": query})
    data = response.json()

    # Center map in the middle of bounding box
    center = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
    m = folium.Map(location=center, zoom_start=14)

    # Add markers
    for el in data['elements']:
        if 'lat' in el and 'lon' in el:
            lat, lon = el['lat'], el['lon']
        elif 'center' in el:
            lat, lon = el['center']['lat'], el['center']['lon']
        else:
            continue

        tags = el.get('tags', {})
        name = tags.get('name', 'Unnamed')

        if tags.get('amenity') == 'gym':
            color = 'red'
        elif tags.get('leisure') == 'fitness_centre':
            color = 'blue'
        else:
            color = 'gray'

        folium.Marker(
            location=[lat, lon],
            popup=name,
            tooltip=name,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    # Generate the HTML of the map
    map_html = m.get_root().render()

    return templates.TemplateResponse("osm_gyms_map.html", {"request": request, "osm_gyms_map_html": map_html})