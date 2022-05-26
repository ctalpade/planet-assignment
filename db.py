from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from constants import dburl

Base = declarative_base()
engine = create_engine(dburl, echo=True, future=True) 

def init():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
