from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean, Date
from flask import Blueprint, render_template, request, current_app, g, make_response
from flask.cli import with_appcontext
from hf1.models import diensten_models, medewerker_models, reserveringen_models, account_models
from hf1.database import db
from datetime import datetime
import random
from hf1.login_functie import *
import json
# import jsonify

dagendict = {
    0:"maandag",
    1:"dinsdag",
    2:"woensdag",
    3:"donderdag",
    4:"vrijdag",
    5:"zaterdag",
    6:"zondag"
}

bp_reserveren = Blueprint('bp_reserveren', __name__, url_prefix='/reserveren',
                          template_folder='templates')

@bp_reserveren.route('/submit/<medewerker>/<datum>', methods=["POST"])
def filter_reserveringen(medewerker, datum): # d0atum, 
    datum = datetime.strptime(datum, '%d-%m-%Y')
    dag = datum.weekday()
    datum = datum.strftime('%Y-%m-%d')

    print(datum)
    print(medewerker)
    
    if medewerker == "Geen voorkeur":
        
        alle_tijdsloten = []
        # per dag is de hoeveelheid tijdsloten verschillend
        if dagendict.get(dag) == "zaterdag":
            alle_tijdsloten = medewerker_models.Tijdslot.query.limit(28)
            print("zaterdag")
            
        elif dagendict.get(dag) == "donderdag":
            alle_tijdsloten = medewerker_models.Tijdslot.query.all()
            print("donderdag")
        else:
            # normale dag
            alle_tijdsloten = medewerker_models.Tijdslot.query.limit(36)
            print("normale dag")
        
        # voeg de tijdsloten die gequeried zijn toe aan de set
        alle_mogelijke_tijdsloten = set()
        for tijdslot in alle_tijdsloten:
            alle_mogelijke_tijdsloten.add(tijdslot.omschrijving)

        print("Geen voorkeur geselecteerd!")
        alle_medewerkers = medewerker_models.Medewerker.query.all()
        mogelijke_tijdsloten = set()
        
        for m in alle_medewerkers:
            if m.voornaam != "Geen voorkeur":
                ## check de tijdsloten dat de medewerkers beschikbaar zijn op de gekozen dag
                beschikbare_tijdsloten = filter_tijdsloten_op_dag_en_reservering(m, dag, datum)
                mogelijke_tijdsloten.update(beschikbare_tijdsloten)
                
                ## check of alle tijdsloten al gevonden zijn. If true, dan break
                verschil_tijdsloten = alle_mogelijke_tijdsloten.difference(mogelijke_tijdsloten)
                # print(len(verschil_tijdsloten))
                if len(verschil_tijdsloten) == 0:
                    break 

        beschikbare_tijdsloten = mogelijke_tijdsloten   

    else:
        #querie voor medewerker
        medewerker = db.session.query(medewerker_models.Medewerker).filter(medewerker_models.Medewerker.voornaam == medewerker).first()
        #querie werkrooster op medewerker, dag en beschikbaarheid
        print("wel een medewerker geselecteerd!")
        print(dag)
        print(datum)
        beschikbare_tijdsloten = filter_tijdsloten_op_dag_en_reservering(medewerker, dag, datum)


    beschikbare_tijdsloten = list(beschikbare_tijdsloten) 
    beschikbare_tijdsloten.sort()
        # resultaat teruggeven naar front end 
    response = make_response(json.dumps(beschikbare_tijdsloten))
    response.content_type = 'application/json'
    return response


def filter_tijdsloten_op_dag_en_reservering(medewerker, dag, datum):
        tijdslot_bezet = set()
        tijdslot_beschikbaar = set()
        dagrooster_medewerker = db.session.query(medewerker_models.Werkrooster).filter(medewerker_models.Werkrooster.medewerker_id == medewerker.id,\
            medewerker_models.Werkrooster.dag == dagendict.get(dag), medewerker_models.Werkrooster.beschikbaarheid_code == "W")
        # convert tijdslot.id naar tijdslot.omschrijving en toevoegen aan tijdslot_beschikbaar
        for selectie in dagrooster_medewerker:
            tijdslot_dagrooster_medewerker = db.session.query(medewerker_models.Tijdslot).filter(medewerker_models.Tijdslot.id == selectie.tijdslot_id).first()
            tijdslot_beschikbaar.add(tijdslot_dagrooster_medewerker.omschrijving)
        
        # print(tijdslot_beschikbaar)

        # query reserveringen op medewerker en datum
        reserveringen = db.session.query(reserveringen_models.Reservering).filter(reserveringen_models.Reservering.medewerker_id == medewerker.id, reserveringen_models.Reservering.datum == datum)
        # convert tijdslot.id naar tijdslot.omschrijving en toevoegen aan tijdslot_bezet
        for res in reserveringen:
            tijdslot = db.session.query(medewerker_models.Tijdslot).filter(medewerker_models.Tijdslot.id == res.tijdslot_id).first()
            tijdslot_bezet.add(tijdslot.omschrijving)
        
        # verschil tussen alle tijdsloten en niet beschikbare tijdsloten vergelijken 
        beschikbare_tijdsloten = tijdslot_beschikbaar.difference(tijdslot_bezet)

        return beschikbare_tijdsloten


@bp_reserveren.route('/submit')
def index():
    overzicht_medewerkers = medewerker_models.Medewerker.query.all()

    if has_cookie('user_id'):
        if not logged_in():
            overzicht_diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
        else:
            overzicht_diensten = diensten_models.Dienst.query.all()
    else:
        overzicht_diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
    #query voor ingelogd, laat pauze wel zien
    overzicht_tijdslot = medewerker_models.Tijdslot.query.all()

    return render_template('reserveren.html',
                           title='reserveren',
                           year=datetime.now().year,
                           message='',
                           diensten= overzicht_diensten,
                           medewerkers = overzicht_medewerkers,
                           tijdslots = overzicht_tijdslot,
                           dienst = '',
                           tijdslot = '',
                           medewerker = '',
                           datum = '')

@bp_reserveren.route('/submit', methods=["POST"])
def post_maak_reservering():
    dienst = request.form['dienst']
    try:
        tijdslot = request.form['tijdslot']
    except: 
        tijdslot = ""
    medewerker = request.form['medewerker']
    datum = request.form['datum']
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    email = request.form['email']
    telefoon = request.form['telefoon']
    # print("Tijdslot: ", tijdslot)
    # print("Medewerker: ", medewerker)
    # print("Datum: ", datum)
    # print("Dienst: ", dienst)

    errors = []
    if len(str(dienst)) < 1:
        errors.append("Geen dienst geselecteerd")
        errors == 1
    if len(str(datum)) < 1:
        errors.append("Geen datum geselecteerd")
    if len(str(medewerker)) < 1:
        errors.append("Geen medewerker geselecteerd")
        errors == 1
    if len(str(tijdslot)) < 1:
        errors.append("Geen tijdslot geselecteerd")
        errors == 1

    if len(voornaam) < 1:
        errors.append("Geen voornaam ingevoerd")
        errors == 1
    if len(achternaam) < 1:
        errors.append("Geen achternaam ingevoerd")
        errors == 1
    if len(email) < 1:
        errors.append("Geen email ingevoerd")
        errors == 1
    if len(telefoon) < 1:
        errors.append("Geen telefoonnummer ingevoerd")
        errors == 1

    # Als er geen errors zijn (dus alle velden zijn correct ingevoerd)
    if len(errors) == 0:
        tijdslot_submit = db.session.query(medewerker_models.Tijdslot).filter(medewerker_models.Tijdslot.omschrijving == tijdslot).first()
        dienst_submit = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.omschrijving == dienst).first()
        
        klant_submit=db.session.query(account_models.Account).filter(account_models.Account.achternaam==achternaam).first()
        print(klant_submit)
        if klant_submit == None:
            klant = account_models.Account(voornaam, achternaam, "", 0, "", "", email, telefoon, "klant") #voeg klant toe
        else:
            klant = klant_submit #gebruik klant_submit als klant in reservering 
        
        # verzander datum in de nodige dag-maand-tijd volgordes en lees de dag uit
        gekozen_datum = datetime.strptime(datum, '%d-%m-%Y')
        dag = gekozen_datum.weekday()
        gekozen_datum = gekozen_datum.strftime('%Y-%m-%d')
        mogelijke_medewerkers = []
        medewerker_submit = []

        # als er geen voorkeur is geselecteerd dan moet er een random worden gekozen
        if medewerker == "Geen voorkeur":
            # query in de medewerkers die op dat moment (tijdslot + dag) beschikbaar zijn
            # query eerst alle medewerkers
            alle_medewerkers = medewerker_models.Medewerker.query.all()

            #voor elke medewerker...
            for m in alle_medewerkers:
                # ... haal hun beschikbare tijdsloten op met de filter functie (zie boven)
                beschikbare_tijdsloten = filter_tijdsloten_op_dag_en_reservering(m, dag, gekozen_datum)
                # als de gekozen tijdslot in die lijst zit, dan is de medewerker dus beschikbaar 
                # (en geen voorkeur mag niet gekozen worden) 
                if tijdslot in beschikbare_tijdsloten and m.voornaam != "Geen voorkeur":
                    mogelijke_medewerkers.append(m)
            
            #kies er een random uit 
            random_medewerker = random.choice(mogelijke_medewerkers)
            medewerker_submit = random_medewerker
        else:
            medewerker_submit = db.session.query(medewerker_models.Medewerker).filter(medewerker_models.Medewerker.voornaam == medewerker).first()
        
        
        
        reservering = reserveringen_models.Reservering(datum=datum, actief=True)
        # dienstoverzicht = reserveringen_models.Dienstenoverzicht()
        # dienstoverzicht.dienst = dienst_submit
        # reservering.diensten.append(dienst_submit)
        dienst_submit.reservering_dienst.append(reservering)
        tijdslot_submit.reservering_tijdslot.append(reservering)
        medewerker_submit.reservering_medewerker.append(reservering)
        klant.reservering_account.append(reservering)

        db.session.add(klant)
        db.session.add(tijdslot_submit)
        db.session.add(medewerker_submit)
        db.session.add(dienst_submit)
        db.session.commit()

    if len(errors) == 0:

        return render_template('reservering_bevestigd.html',
                            title='Bevestiging',                           
                            dienst=dienst,
                            tijdslot=tijdslot,
                            medewerker=medewerker_submit.voornaam,
                            datum=datum)

    else:   
        overzicht_medewerkers = medewerker_models.Medewerker.query.all()
        overzicht_diensten = diensten_models.Dienst.query.all()
       
        if has_cookie('user_id'):
            if not logged_in():
                overzicht_diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
                overzicht_tijdslot = db.session.query(medewerker_models.Tijdslot).all()
                return render_template('reserveren.html',
                            title='reserveren',
                            year=datetime.now().year,
                            message='',
                            diensten= overzicht_diensten,
                            medewerkers = overzicht_medewerkers,
                            tijdslots = overzicht_tijdslot,
                            dienst = overzicht_diensten,
                            tijdslot = '',
                            medewerker = '',
                            datum = '',
                            errors=errors,
                            voornaam=voornaam,
                            achternaam=achternaam,
                            email=email,
                            telefoon=telefoon)
            else:
                overzicht_diensten = diensten_models.Dienst.query.all()
                overzicht_tijdslot = db.session.query(medewerker_models.Tijdslot).all()
                return render_template('reserveren.html',
                            title='reserveren',
                            year=datetime.now().year,
                            message='',
                            diensten= overzicht_diensten,
                            medewerkers = overzicht_medewerkers,
                            tijdslots = overzicht_tijdslot,
                            dienst = overzicht_diensten,
                            tijdslot = '',
                            medewerker = '',
                            datum = '',
                            errors=errors,
                            voornaam=voornaam,
                            achternaam=achternaam,
                            email=email,
                            telefoon=telefoon)

        else:
            overzicht_diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
            #query voor ingelogd, laat pauze wel zien
            overzicht_tijdslot = db.session.query(medewerker_models.Tijdslot).all()
        
            return render_template('reserveren.html',
                            title='reserveren',
                            year=datetime.now().year,
                            message='',
                            diensten= overzicht_diensten,
                            medewerkers = overzicht_medewerkers,
                            tijdslots = overzicht_tijdslot,
                            dienst = overzicht_diensten,
                            tijdslot = '',
                            medewerker = '',
                            datum = '',
                            errors=errors,
                            voornaam=voornaam,
                            achternaam=achternaam,
                            email=email,
                            telefoon=telefoon)

        # return render_template('reserveren.html',
        #                 title='Reserveren is niet gelukt',                           
        #                 dienst=overzicht_diensten,
        #                 tijdslot=overzicht_tijdslot,
        #                 medewerker=overzicht_medewerkers,
        #                 datum=datum,
        #                 errors=errors) 
