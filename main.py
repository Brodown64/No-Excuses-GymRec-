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
import requests
import folium

import sys
import os
import json
import pathlib
import geopandas as gpd 
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from branca.element import Element

ox.__version__

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

bbox = [40.70, -74.02, 40.78, -73.95] 

app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
# resize image

class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

class UserLocation(BaseModel):
    latitude: float
    longitude: float

style = Element("""
    <style>
    .folium-map {
        height: 40vh !important;
        width: 50% !important;
    }
</style>
""")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    # m = Map()
    # return m.get_root().render()

@app.get("/map", response_class=HTMLResponse)
async def show_map(request: Request):
    return templates.TemplateResponse("dynamic_map.html", {"request": request}) # problem child