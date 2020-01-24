import click
from flask import current_app, g
from flask.cli import with_appcontext
from hf1.models import account_models, artikel_models, medewerker_models, diensten_models, orderoverzicht_models, \
    reserveringen_models
from hf1.database import db
from hf1.load_data_from_file import load_data_csv
from hf1.werkrooster_rooster_inladen import *


def init_db():
    db.create_all()


def fill_db():
    db.drop_all()
    db.create_all()

    db.session.add(medewerker_models.Tijdslot("09:00"))
    db.session.add(medewerker_models.Tijdslot("09:15"))
    db.session.add(medewerker_models.Tijdslot("09:30"))
    db.session.add(medewerker_models.Tijdslot("09:45"))
    db.session.add(medewerker_models.Tijdslot("10:00"))
    db.session.add(medewerker_models.Tijdslot("10:15"))
    db.session.add(medewerker_models.Tijdslot("10:30"))
    db.session.add(medewerker_models.Tijdslot("10:45"))
    db.session.add(medewerker_models.Tijdslot("11:00"))
    db.session.add(medewerker_models.Tijdslot("11:15"))
    db.session.add(medewerker_models.Tijdslot("11:30"))
    db.session.add(medewerker_models.Tijdslot("11:45"))
    db.session.add(medewerker_models.Tijdslot("12:00"))
    db.session.add(medewerker_models.Tijdslot("12:15"))
    db.session.add(medewerker_models.Tijdslot("12:30"))
    db.session.add(medewerker_models.Tijdslot("12:45"))
    db.session.add(medewerker_models.Tijdslot("13:00"))
    db.session.add(medewerker_models.Tijdslot("13:15"))
    db.session.add(medewerker_models.Tijdslot("13:30"))
    db.session.add(medewerker_models.Tijdslot("13:45"))
    db.session.add(medewerker_models.Tijdslot("14:00"))
    db.session.add(medewerker_models.Tijdslot("14:15"))
    db.session.add(medewerker_models.Tijdslot("14:30"))
    db.session.add(medewerker_models.Tijdslot("14:45"))
    db.session.add(medewerker_models.Tijdslot("15:00"))
    db.session.add(medewerker_models.Tijdslot("15:15"))
    db.session.add(medewerker_models.Tijdslot("15:30"))
    db.session.add(medewerker_models.Tijdslot("15:45"))
    db.session.add(medewerker_models.Tijdslot("16:00"))
    db.session.add(medewerker_models.Tijdslot("16:15"))
    db.session.add(medewerker_models.Tijdslot("16:30"))
    db.session.add(medewerker_models.Tijdslot("16:45"))
    db.session.add(medewerker_models.Tijdslot("17:00"))
    db.session.add(medewerker_models.Tijdslot("17:15"))
    db.session.add(medewerker_models.Tijdslot("17:30"))
    db.session.add(medewerker_models.Tijdslot("17:45"))
    db.session.add(medewerker_models.Tijdslot("18:00"))
    db.session.add(medewerker_models.Tijdslot("18:15"))
    db.session.add(medewerker_models.Tijdslot("18:30"))
    db.session.add(medewerker_models.Tijdslot("18:45"))
    db.session.add(medewerker_models.Tijdslot("19:00"))
    db.session.add(medewerker_models.Tijdslot("19:15"))
    db.session.add(medewerker_models.Tijdslot("19:30"))
    db.session.add(medewerker_models.Tijdslot("19:45"))
    db.session.add(medewerker_models.Tijdslot("20:00"))
    db.session.add(medewerker_models.Tijdslot("20:15"))
    db.session.add(medewerker_models.Tijdslot("20:30"))
    db.session.add(medewerker_models.Tijdslot("20:45"))

    # load data from FILE into TABLE
    # TEST DATA DIENSTEN, ARTIKELEN, MEDEWERKERS (DEZE VERANDEREN OP DIT MOMENT NIET)
    load_data_csv('hf1/externe_data/diensten.csv', diensten_models.Dienst.__tablename__)
    load_data_csv('hf1/externe_data/medewerker.csv', medewerker_models.Medewerker.__tablename__)
    load_data_csv('hf1/externe_data/artikelen.csv', artikel_models.Artikel.__tablename__)
    load_data_csv('hf1/externe_data/artikelgroep.csv', artikel_models.Artikelgroep.__tablename__)
    # load_data_csv('hf1/externe_data/test_reserveringen.csv', reserveringen_models.Reservering.__tablename__)

    werkrooster_inladen()

    # test data account
    new_account = account_models.Account(
        "Stijn", "vanBienvanBuurkes", "nlala", 11, "8888AD", "Valkenswird", "leon@live.nl", 62222222, "klant")
    db.session.add(new_account)

    new_mod = account_models.Account("Medewerker", "Medewerker", "", "", "", "", "medewerker@hairforce1.nl", "", "medewerker")
    db.session.add(new_mod)

    new_admin = account_models.Account("Manager", "Manager", "", "", "", "", "manager@hairforce1.nl", "","manager")
    db.session.add(new_admin)

    # ADD THE LINK BETWEEN ARTIKEL AND ARTIKELGROUP (needed to generate association table)
    # gel = artikel_models.Artikelgroep("Gel")
    # for artikel in artikel_models.Artikel.query.all():
    #     artikel.artikelgroep = gel

    # mederwerker_bla = medewerker_models.Medewerker("Stijn", "Test")
    # db.session.add(mederwerker_bla)
    # medewerker_stijn = db.session.query(medewerker_models.Medewerker).filter(medewerker_models.Medewerker.voornaam == "Jasmin").first()
    # medewerker_stijn.tijdsloten.append(medewerker_models.Tijdslot("1200-1300"))
    # medewerker_stijn.tijdsloten.append(medewerker_models.Tijdslot("1300-1400"))

    # TEST DATA RESERVERGING
    # CREATE LINK BETWEEN RESERVERING AND DIENST (with the use of association table DIENSTENOVERZICHT)
    # search for specific 'dienst'
    # dienst =  db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.omschrijving == "turpis").first()
    # add this dienst to the specific 'reservering'
    # diensten_overzicht = reserveringen_models.Dienstenoverzicht()
    # diensten_overzicht.dienst = dienst
    # reserveringen_parent = reserveringen_models.Reservering(tijdslots=3)
    # reserveringen_parent.diensten.append(diensten_overzicht)
    # medewerker_stijn.reservering_medewerker.append(reserveringen_parent)
    # new_account.reservering_account.append(reserveringen_parent)
    # db.session.add(medewerker_stijn)
    # db.session.add(new_account)

    # TODO orderartikel data aanmaken

    # shampoo = artikel_models.Artikelgroep("bla")
    # hens = artikel_models.Artikel(shampoo, "bla", 11)
    # order = orderoverzicht_models.Orderoverzicht(50)
    # order_artikel = orderoverzicht_models.Order_Artikel(hoeveelheid_artikel=20)
    # order_artikel.child = hens
    # order.children.append(order_artikel)
    # db.session.add(order)





    db.session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database %s.' %
               current_app.config['SQLALCHEMY_DATABASE_URI'])


@click.command('fill-db')
@with_appcontext
def fill_db_command():
    """Clear the existing data and create new tables."""
    fill_db()
    click.echo('Cleaning and added test data to database %s.' %
               current_app.config['SQLALCHEMY_DATABASE_URI'])


def init_cli_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(fill_db_command)