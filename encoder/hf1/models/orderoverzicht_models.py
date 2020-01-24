from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from datetime import datetime
from hf1.database import db

# kopple table (order artikel)
class Order_Artikel(db.Model):
    __tablename__ = 'order_artikelen'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    artikel_id = Column(Integer, ForeignKey('artikelen.id'), primary_key=True)
    hoeveelheid_artikel = Column(Integer)
    child = relationship("Artikel")


# parent
class Orderoverzicht(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    children = relationship("Order_Artikel")
    totaalprijs = Column(Float(100), nullable=False) # moet nog over nagedacht worden welke type deze data is
    datum = Column(DateTime)
    klant_id = Column(Integer, ForeignKey("accounts.id"))

    def __init__(self, totaalprijs):
        self.totaalprijs = totaalprijs
        self.datum = datetime.utcnow()


    def __repr__(self):
        return '<Orderoverzicht %r>' % (self.artikelen)
