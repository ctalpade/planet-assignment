from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///test.db", echo=True, future=True) 

import model.allmodels

def init():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
