from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime
from hf1.database import db


class Account(db.Model):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    voornaam = Column(String(100), nullable=False)
    achternaam = Column(String(100), nullable=False)
    straatnaam = Column(String(100), nullable=False)
    huisnummer = Column(Integer, nullable=False)
    postcode = Column(Integer, nullable=False)
    woonplaats = Column(String(100), nullable=False)
    telefoon = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    toevoeging = Column(String(100), nullable=True)
    wachtwoord = Column(String(100), nullable=True)
    reservering_account = relationship("Reservering")
    user_role = Column(String(15), nullable=False)

    # TODO: order in order.id vervangen met de naam van order tabel + "Parent" vervangen met dezelfde naam
    # parent_id = Column(Integer, ForeignKey('order.id'))
    # parent = relationship("Parent", back_populates="accounts")
    aanmaak_datum = Column(Date)

    def __init__(self, voornaam, achternaam, straatnaam, huisnummer, postcode, woonplaats, email, telefoon, user_role):
        self.achternaam = achternaam
        self.voornaam = voornaam
        self.straatnaam = straatnaam
        self.huisnummer = huisnummer
        self.postcode = postcode
        self.woonplaats = woonplaats
        self.telefoon = telefoon
        self.email = email
        self.toevoeging = ""
        # self.orderIDs = orderIDs
        self.aanmaak_datum = datetime.utcnow()
        self.wachtwoord = ""
        self.user_role = user_role

    def __repr__(self):
        return '<Account %r>' % (self.email)
