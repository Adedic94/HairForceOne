from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, DateTime, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from hf1.database import db

# MEDEWERKER EN TIJDSLOT HEBBEN EEN many-to-many RELATIONSHIP

# DEZE TABEL DEFINIEERT DE RELATIE TUSSEN MEDEWERKER EN TIJDSLOT
beschikbaarheid = Table('beschikbaarheid', db.Model.metadata,
                        Column('Medewerker', Integer,
                               ForeignKey('medewerkers.id')),
                        Column('Tijdslot', Integer,
                               ForeignKey('tijdsloten.id'))
                        )


class Medewerker(db.Model):
    # MEDEWERKER IS DE PARENT VAN TIJDSLOT
    __tablename__ = 'medewerkers'
    id = Column(Integer, primary_key=True)
    voornaam = Column(String(100), nullable=False)
    achternaam = Column(String(100), nullable=False)
    tijdsloten = relationship("Tijdslot", secondary=beschikbaarheid) #zorg dat deze class de juiste tabel kent
    reservering_medewerker = relationship("Reservering")
    werkrooster_medewerker = relationship("Werkrooster")

    def __init__(self, voornaam, achternaam):
        self.achternaam = achternaam
        self.voornaam = voornaam

    def __repr__(self):
        return '<Medewerker %r>' % (self.voornaam)

#TIJDSLOT IS DE CHILD VAN MEDEWERKER
class Tijdslot(db.Model):
    __tablename__ = 'tijdsloten'
    id = Column(Integer, primary_key=True)
    omschrijving = Column(String(100), nullable=False)
    reservering_tijdslot = relationship("Reservering")
    werkrooster_tijdslot = relationship("Werkrooster")

    def __init__(self, omschrijving):
        self.omschrijving = omschrijving
        
    def __repr__(self):
        return '<Tijdslot %r>' % (self.omschrijving)

class Werkrooster_CSV(db.Model):
    __tablename__ = 'werkrooster_CSV'
    id = Column(Integer, primary_key=True)
    medewerker_rooster=Column(String(100), nullable=False)
    rooster=Column(String(100), nullable=False)

    def __init__(self, omschrijving):
        self.medewerker_rooster = medewerker_rooster
        
    def __repr__(self):
        return '<Werkrooster_CSV %r>' % (self.medewerker_rooster)


class Werkrooster(db.Model):
    __tablename__ = 'werkrooster'
    id = Column(Integer, primary_key=True)
    medewerker_id = Column(Integer, ForeignKey("medewerkers.id"))
    tijdslot_id = Column(Integer, ForeignKey("tijdsloten.id"))
    dag=Column(String(100), nullable=False)
    beschikbaarheid_code=Column(String(100), nullable=False)

    def __init__(self, dag, beschikbaarheid_code):
        self.dag = dag
        self.beschikbaarheid_code = beschikbaarheid_code
        
    def __repr__(self):
        return '<Tijdslot %r>' % (self.beschikbaarheid_code)
