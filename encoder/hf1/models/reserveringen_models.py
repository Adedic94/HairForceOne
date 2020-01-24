from datetime import datetime

from sqlalchemy import Column, Integer, String, Table, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from hf1.database import db

# RESERVERINGEN EN DIENSTEN HEBBEN EEN many-to-many RELATIONSHIP

# DEZE TABEL DEFINIEERT DE RELATIE TUSSEN RESERVERINGEN EN DIENST
# class Dienstenoverzicht(db.Model):
#     __tablename__ = 'dienstenoverzichten'
#     reserveringen_id = Column(Integer, ForeignKey('reserveringen.id'), primary_key=True)
#     diensten_id = Column(Integer, ForeignKey('diensten.id'), primary_key=True)
#     dienst = relationship("Dienst")


class Reservering(db.Model):
    # Reservering is PARENT van: Dienst, Tijdslot, Medewerker en Klant
    __tablename__ = 'reserveringen'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True) 
    tijdslot_id = Column(Integer, ForeignKey("tijdsloten.id")) #Link leggen naar tijdsloten tabel
    dienst_id = Column(Integer, ForeignKey("diensten.id"))
    # dienst = relationship("Dienst") #zorg dat deze class de juiste tabel kent
    medewerker_id = Column(Integer, ForeignKey("medewerkers.id"))
    klant_id = Column(Integer, ForeignKey("accounts.id"))
    datum=Column(Date, nullable=False)
    actief=Column(Boolean, nullable=False)
    

    def __init__(self, datum, actief):
        self.aanmaak_datum = datetime.utcnow()
        self.datum=datetime.strptime(datum, '%d-%m-%Y')
        self.actief=actief
        

    def __repr__(self):
        return '<Reservering %r>' % (self.id)

    # Put the below into cli.py, still needs to be automated
    '''knippen = diensten_models.Dienst("knippen", 18.0, 1)
    kleuren = diensten_models.Dienst("kleuren", 60.0, 2)

    db.session.add(knippen)
    db.session.add(kleuren)
    db.session.add(diensten_models.Dienst("fohn", 10.0, 1))
    db.session.add(diensten_models.Dienst("permanent", 60.0, 3))
    db.session.add(diensten_models.Dienst("watergolven", 60.0, 2))

    # test data reservering nummer 1
    reserveringen_parent = reserveringen_models.Reservering(tijdslots=3, medewerker="Leon", klant="Evert" + " Mulder")

    # voeg knippen toe aan reservering 1 in dienstoverzicht
    dienst_overzicht = reserveringen_models.Dienstenoverzicht()
    dienst_overzicht.child = knippen
    reserveringen_parent.diensten.append(dienst_overzicht)
    db.session.add(reserveringen_parent)

    # voeg kleuren toe aan reservering 1 in dienstoverzicht
    dienst_overzicht = reserveringen_models.Dienstenoverzicht()
    dienst_overzicht.child = kleuren
    reserveringen_parent.diensten.append(dienst_overzicht)
    db.session.add(reserveringen_parent)'''