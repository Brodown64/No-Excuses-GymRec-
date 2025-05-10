from fastapi import FastAPI, Request, Header, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr

import json
import pathlib

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
# fix problem with DB (check docs section of website to see error)

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

class UserLocation(BaseModel):
    latitude: float
    longitude: float

@app.get("/")
async def root(request: Request, db: Session = Depends(get_db)):
    gyms = crud.get_gyms(db)
    return templates.TemplateResponse("index.html", {"request": request, "gyms": gyms})
    return {"message": "Hello World"}

@app.post("/gyms/", response_model=schemas.Gym)
def add_gym(gym: schemas.GymCreate, db: Session = Depends(get_db)):
    return crud.create_gym(db, gym)

@app.get("/gyms/", response_model=list[schemas.Gym])
def list_gyms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_gyms(db, skip=skip, limit=limit)

@app.post("/location/")
async def create_location(location: UserLocation):
    
    return {"received_latitude": location.latitude, "received_longitude": location.longitude}
