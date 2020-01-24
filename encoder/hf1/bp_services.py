from flask import Blueprint, render_template, request, make_response
from hf1.models import diensten_models
from hf1.database import db
from datetime import datetime
from hf1.login_functie import *
import json

bp_services = Blueprint('bp_services', __name__, url_prefix='/services',
                        template_folder='templates')


@bp_services.route('/')
def index():
    if has_cookie('user_id'):
        if not logged_in():
            ingelogd = False
        else:
            if user_is_manager(session["id"]):
                ingelogd = True
            else:
                ingelogd = False
    else:
        ingelogd = False

    diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
    return render_template('diensten.html',
                           title='Behandelingen',
                           year=datetime.now().year,
                           message='Onze behandelingen',
                           diensten=diensten,
                           ingelogd=ingelogd)

@bp_services.route('/aanpassen')
def show_diensten_edit():
    diensten = diensten_models.Dienst.query.all()
    return render_template('diensten_edit.html',
                           title='Behandelingen',
                           year=datetime.now().year,
                           message='Onze behandelingen',
                           diensten=diensten)

@bp_services.route('/aanpassen/submit', methods=["POST"])
def update_diensten_tabel():
    dienst = request.form['diensten_tabel']
    data  = json.loads(dienst)
    

    diensten_models.Dienst.query.delete()
    new_id = 0
    for entry in data:
        omschrijving = entry[0]
        prijs = entry[1]
        print(prijs)
        try:
            prijs = float(prijs.replace(',', '.'))
        except ValueError:
            prijs="0.0"
            
        duur = entry[2]
        vervallen = bool((entry[3]=="True"))
        new_entry= diensten_models.Dienst(omschrijving, prijs, duur, vervallen)
        new_entry.id =new_id
        new_id += 1
        db.session.add(new_entry)
    db.session.commit()
    exists = db.session.query(diensten_models.Dienst.id).filter_by(omschrijving='Pauze').scalar()
    if exists == None:
        pauze_entry = diensten_models.Dienst("Pauze", "0.0", 0, False)
        pauze_entry.id = new_id+1
        db.session.add(pauze_entry)
        db.session.commit()
       
    res = make_response("datainvoer test " + dienst)

    diensten = diensten_models.Dienst.query.all()

    if has_cookie('user_id'):
        if not logged_in():
            ingelogd = False
        else:
            if user_is_manager(session["id"]):
                ingelogd = True
            else:
                ingelogd = False
    else:
        ingelogd = False
    return render_template('diensten.html',
                           title='Behandelingen',
                           year=datetime.now().year,
                           message='Onze behandelingen',
                           diensten=diensten,
                           ingelogd=ingelogd)

@bp_services.route('/Wasmassage_knippen_stylen')
def Wasmassage_knippen_stylen():

    if has_cookie('user_id'):
        if not logged_in():
            ingelogd = False
        else:
            if user_is_manager(session["id"]):
                ingelogd = True
            else:
                ingelogd = False
    else:
        ingelogd = False

    diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
    return render_template('Wasmassage_knippen_stylen.html',
                           title='Behandelingen',
                           year=datetime.now().year,
                           message='Onze behandelingen',
                           diensten=diensten,
                           ingelogd=ingelogd)
    
@bp_services.route('/modelföhnen')
def modelföhnen():

    if has_cookie('user_id'):
        if not logged_in():
            ingelogd = False
        else:
            if user_is_manager(session["id"]):
                ingelogd = True
            else:
                ingelogd = False
    else:
        ingelogd = False

    diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
    return render_template('modelföhnen.html',
                           title='Behandelingen',
                           year=datetime.now().year,
                           message='Onze behandelingen',
                           diensten=diensten,
                           ingelogd=ingelogd)   

@bp_services.route('/kleuren_balayage_highlights ')
def kleuren_balayage_highlights():

    if has_cookie('user_id'):
        if not logged_in():
            ingelogd = False
        else:
            if user_is_manager(session["id"]):
                ingelogd = True
            else:
                ingelogd = False
    else:
        ingelogd = False

    diensten = db.session.query(diensten_models.Dienst).filter(diensten_models.Dienst.vervallen == True).all()
    return render_template('kleuren_balayage_highlights.html',
                           title='Behandelingen',
                           year=datetime.now().year,
                           message='Onze behandelingen',
                           diensten=diensten,
                           ingelogd=ingelogd)   
       
