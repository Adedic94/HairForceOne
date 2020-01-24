from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean, Date
from sqlalchemy.orm import relationship

from datetime import datetime
from hf1.database import db

# # TODO is dit een database??
# class Dienstenoverzicht(db.Model):
#     __tablename__ = 'dienstenoverzicht'
#     id = Column(Integer, primary_key=True)
#     #TODO is dit nodig?
#     #diensten = relationship('Dienst')
#     #diensten = Column(ARRAY(Integer), nullable = False)
#     omschrijving = Column(String(250), nullable=False)
#     aanmaak_datum = Column(DateTime)
#     totaal_tijdsslot = Column(Integer)

#     def __init__(self, omschrijving):
#         self.omschrijving = omschrijving
#         self.aanmaak_datum = datetime.utcnow()

#     def __repr__(self):
#         return '<Artikelgroep %r>' % (self.omschrijving)

#DIENST IS DE CHILD VAN RESERVERINGEN
class Dienst(db.Model):
    __tablename__ = 'diensten'
    id = Column(Integer, primary_key=True)
    reservering_dienst = relationship("Reservering")
    omschrijving = Column(String(250), nullable=False)
    prijs = Column(Float)
    aanmaak_datum = Column(Date, nullable=False)
    vervallen = Column(Boolean, nullable=False)
    hoeveelheid_tijdslot = Column(Integer,  nullable=False)

    def __init__(self, omschrijving, prijs, duur, vervallen):
        self.omschrijving = omschrijving
        self.hoeveelheid_tijdslot = duur
        self.prijs = prijs
        self.aanmaak_datum = datetime.utcnow()
        self.vervallen = vervallen

    def __repr__(self):
        return '<Dienst %r>' % (self.omschrijving)