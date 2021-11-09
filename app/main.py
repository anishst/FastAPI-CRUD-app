# https://codingnomads.co/blog/python-fastapi-tutorial
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer
import pymongo
import json
import requests
import subprocess
import os
import pandas as pd
from bson import json_util
from dotenv import load_dotenv # https://pypi.org/project/python-dotenv/
# load env vars - https://www.twilio.com/blog/environment-variables-python
load_dotenv()

app = FastAPI()

# SqlAlchemy Setup https://fastapi.tiangolo.com/tutorial/sql-databases/
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# A SQLAlchemny ORM Place
class DBPlace(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String, nullable=True)
    coffee = Column(Boolean)
    wifi = Column(Boolean)
    food = Column(Boolean)
    lat = Column(Float)
    lng = Column(Float)

Base.metadata.create_all(bind=engine)

# A Pydantic Place
class Place(BaseModel):
    name: str
    description: Optional[str] = None
    coffee: bool
    wifi: bool
    food: bool
    lat: float
    lng: float

    class Config:
        orm_mode = True

# Methods for interacting with the database
def get_place(db: Session, place_id: int):
    return db.query(DBPlace).where(DBPlace.id == place_id).first()

def get_places(db: Session):
    return db.query(DBPlace).all()

def create_place(db: Session, place: Place):
    db_place = DBPlace(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place

# Routes for interacting with the API
@app.post('/places/', response_model=Place)
def create_places_view(place: Place, db: Session = Depends(get_db)):
    db_place = create_place(db, place)
    return db_place

@app.get('/places/', response_model=List[Place])
def get_places_view(db: Session = Depends(get_db)):
    return get_places(db)

@app.get('/place/{place_id}')
def get_place_view(place_id: int, db: Session = Depends(get_db)):
    return get_place(db, place_id)

@app.get("/flight_prices/")
def get_flight_prices():
    try:
        database_url = os.getenv('DATABASE_URL')
        client = pymongo.MongoClient(database_url)
        mydb = client['airline_fares']
        my_collection = mydb['price_history']
        items = my_collection.find({}).sort("script_time", -1)
        # using json util to avoid error: TypeError: ObjectId('') is not JSON serializable
        # https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html
        return json.loads(json_util.dumps(items))
    except Exception as e:
        return f"No data found {e}"

@app.get('/')
async def root():
    return {'message': 'Hello World!'}

@app.get('/dict')
async def dict():
    # df = pd.read_excel('app/data/english_dictionary.xlsx',nrows= 20)
    # return df.head().to_json(indent=2)
    df = pd.read_csv('app/data/english_dictionary.csv')
    return df.tail(2).to_json()