from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hf1.database import db
from hf1.load_data_from_file import load_data_csv
from hf1.models import medewerker_models

def werkrooster_inladen():
    # CSV rooster file wordt ingeladen in Werkrooster_CSV
    load_data_csv('hf1/externe_data/Documentatie_Personeel_en_rooster_csv.csv', medewerker_models.Werkrooster_CSV.__tablename__)
    werkrooster_rows = db.session.query(medewerker_models.Werkrooster_CSV).count()
    # For loop loopt langs alle medewerkers 
    for medewerker in range(werkrooster_rows):
        werkrooster = db.session.query(medewerker_models.Werkrooster_CSV).filter(medewerker_models.Werkrooster_CSV.id == medewerker).first()
        werkrooster_str = str(werkrooster.rooster)
        tijdslot = 0
        tijdslot_lang = 0 # tijdslot var voor donderdag tot 20:00
        tijdslot_kort = 0 # tijdslot var voor zaterdag tot 16:00
        # For loop loopt langs tijdsloten in het rooster (per uur) 
        for x in range(len(werkrooster_str)):
            if x <= 8:
                # For loop verdeelt uren in kwartieren
                for y in range(4):
                    tijdslot += 1
                    werkrooster_add_db(tijdslot, medewerker, "dinsdag", werkrooster_str[x])
            elif x >= 9 and x <= 17:
                if(tijdslot > 35):
                    tijdslot = 0
                for y in range(4):
                    tijdslot += 1
                    werkrooster_add_db(tijdslot, medewerker, "woensdag", werkrooster_str[x])
            elif x >= 18 and x <= 28:
                for y in range(4):
                    tijdslot_lang += 1
                    werkrooster_add_db(tijdslot_lang, medewerker, "donderdag", werkrooster_str[x])
            elif x >= 29 and x <= 37:
                if(tijdslot > 35):
                    tijdslot = 0
                for y in range(4):
                    tijdslot += 1
                    werkrooster_add_db(tijdslot, medewerker, "vrijdag", werkrooster_str[x])
            elif x >= 38 and x <= 44:
                for y in range(4):
                    tijdslot_kort += 1
                    werkrooster_add_db(tijdslot_kort, medewerker, "zaterdag", werkrooster_str[x])

def werkrooster_add_db(tijdslot_id, medewerker_id, dag, beschikbaarheid_code):
    #standaard append zie reserveringen tabel
    tijdslot_parent = db.session.query(medewerker_models.Tijdslot).filter(medewerker_models.Tijdslot.id == tijdslot_id).first()
    medewerker_parent = db.session.query(medewerker_models.Medewerker).filter(medewerker_models.Medewerker.id == medewerker_id).first()
    werkrooster_overzicht = medewerker_models.Werkrooster(dag, beschikbaarheid_code)
    
    tijdslot_parent.werkrooster_tijdslot.append(werkrooster_overzicht)
    medewerker_parent.werkrooster_medewerker.append(werkrooster_overzicht)

    db.session.add(tijdslot_parent, medewerker_parent)