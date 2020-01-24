from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean, Date
from sqlalchemy.orm import relationship

from datetime import datetime
from hf1.database import db

class Artikelgroep(db.Model):
    __tablename__ = 'artikelgroepen'
    id = Column(Integer, primary_key=True)
    artikelen = relationship('Artikel')
    omschrijving = Column(String(250), nullable=False)

    def __init__(self, omschrijving):
        self.omschrijving = omschrijving

    def __repr__(self):
        return '<Artikelgroep %r>' % (self.omschrijving)


class Artikel(db.Model):
    __tablename__ = 'artikelen'
    id = Column(Integer, primary_key=True)
    artikelgroep_id = Column(Integer, ForeignKey('artikelgroepen.id'))
    artikelgroep = relationship(Artikelgroep)
    omschrijving = Column(String(250), nullable=False)
    actuele_voorraad = Column(Integer, nullable=False)
    gewenste_minimale_voorraad = Column(Integer)
    gewenste_maximale_voorraad = Column(Integer)
    backorder_voorraad = Column(Integer)
    advies_verkoopprijs = Column(Float)
    aanmaak_datum = Column(Date, nullable=False)
    vervallen = Column(Boolean, nullable=False)

    def __init__(self, artikelgroep, omschrijving, advies_verkoopprijs):
        self.omschrijving = omschrijving
        self.artikelgroep = artikelgroep
        self.actuele_voorraad = 0
        self.gewenste_minimale_voorraad = 0
        self.gewenste_maximale_voorraad = 0
        self.backorder_voorraad = 0
        self.advies_verkoopprijs = 0.0
        self.advies_verkoopprijs = advies_verkoopprijs
        self.aanmaak_datum = datetime.utcnow()
        self.vervallen = False

    def __repr__(self):
        return '<Artikel %r>' % (self.omschrijving)