from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hf1.database import db
import csv
import pandas as pd

test = "string"
def Load_Data(file_name):
    data = csv.reader(file_name, delimiter=',')# skiprows=1, converters={0: lambda s: str(s)})
    return data.tolist()

class Test_Tabel(db.Model):
    __tablename__ = 'test_tabel'
    id = Column(Integer, primary_key=True)
    omschrijving = Column(String(250), nullable=False)
    prijs = Column(Float)
    aanmaak_datum = Column(Date, nullable=False)
    vervallen = Column(Boolean, nullable=False)
    hoeveelheid_tijdsslot = Column(Integer,  nullable=False) 

    def __init__(self, omschrijving, prijs, duur):
        self.omschrijving = omschrijving
        self.hoeveelheid_tijdsslot = duur
        self.prijs = prijs
        self.aanmaak_datum = datetime.utcnow()
        self.vervallen = False

    def __repr__(self):
        return '<Dienst %r>' % (self.omschrijving)

def load_data_csv(file_name, table_name):
    engine = create_engine('sqlite:///instance/hf1.db')
    # file_name = 'hf1/externe_data/test_diensten.csv'
    df = pd.read_csv(file_name)
    df.to_sql(con=engine, index_label = 'id', name=table_name, if_exists='replace', index = True)

