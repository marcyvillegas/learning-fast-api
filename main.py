from fastapi import FastAPI,Query,Depends
from sqlalchemy import Column,String,Integer
from pydantic import BaseModel
from db import engine,sessionLocal,base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

app = FastAPI()


class City(base):
    __tablename__ = 'city'
    id:  Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(30))
    countrycode: Mapped[str] = mapped_column(String(30))
    district: Mapped[str] = mapped_column(String(30))
    population: Mapped[str] = mapped_column(String(30))

class CitySchema(BaseModel):
    id: int
    name: str
    countrycode: str
    district: str
    population: str

    class Config:
        orm_model=True

base.metadata.create_all(bind=engine)

@app.get("/cities")
def get_all_cities():
    db = sessionLocal()
    cities = db.query(City).all()
    db.close()
    return cities
