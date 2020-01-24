from flask import Blueprint, render_template, request, current_app, g, make_response, jsonify
from hf1.models import account_models, diensten_models, medewerker_models, reserveringen_models
from hf1.database import db
from datetime import datetime
from hf1.login_functie import *
import json

bp_rooster = Blueprint('bp_rooster', __name__, url_prefix='/rooster',
                        template_folder='templates')


@bp_rooster.route('/')
def index():
    if has_cookie('user_id'):
        if not logged_in():
            return render_template("login_error.html")
        else:
            if user_is_manager(session["id"]) or user_is_medewerker(session["id"]):
                manager = False
                if user_is_manager(session["id"]):
                    manager = True
                rooster = medewerker_models.Werkrooster.query.all()
                overzicht_tijdslot = medewerker_models.Tijdslot.query.all()
                overzicht_medewerkers = medewerker_models.Medewerker.query.all()
                return render_template('rooster.html',
                                    title='Werkrooster',
                                    year=datetime.now().year,
                                    message='',
                                    rooster=rooster,
                                    overzicht_tijdslot=overzicht_tijdslot,
                                    overzicht_medewerkers=overzicht_medewerkers,
                                    manager=manager)
            else:
                return render_template("login_error.html")
    else:
        return render_template("login_error.html")

@bp_rooster.route('/submit/<medewerker>', methods=["POST"])
def filter_rooster(medewerker):
    # print(medewerker)
    werkrooster = db.session.query(medewerker_models.Werkrooster).filter(medewerker_models.Werkrooster.medewerker_id == medewerker).all()
    # rooster_count = db.session.query(medewerker_models.Werkrooster).filter(medewerker_models.Werkrooster.medewerker_id == medewerker).count()
    json_bericht = []
    for rooster in werkrooster:
        medewerker = db.session.query(medewerker_models.Medewerker).filter(medewerker_models.Medewerker.id == rooster.medewerker_id).first()
        tijdslot = db.session.query(medewerker_models.Tijdslot).filter(medewerker_models.Tijdslot.id == rooster.tijdslot_id).first()

        rooster_dict = {}
        rooster_dict["medewerker_naam"] = medewerker.voornaam
        rooster_dict["medewerker_achternaam"] = medewerker.achternaam
        rooster_dict["tijdslot_omschrijving"] = tijdslot.omschrijving
        rooster_dict["dag"] = rooster.dag
        rooster_dict["beschikbaarheid_code"] = rooster.beschikbaarheid_code
        json_bericht.append(rooster_dict)
    return jsonify(json_bericht)


@bp_rooster.route('/aanpassen')
def rooster_edit():
    if has_cookie('user_id'):
        if not logged_in():
            return render_template("login_error.html")
        else:
            if user_is_manager(session["id"]):
                rooster = medewerker_models.Werkrooster.query.all()
                overzicht_tijdslot = medewerker_models.Tijdslot.query.all()
                overzicht_medewerkers = medewerker_models.Medewerker.query.all()
                return render_template('rooster_edit.html',
                                    title='Rooster aanpassen',
                                    year=datetime.now().year,
                                    message='',
                                    rooster=rooster,
                                    overzicht_tijdslot=overzicht_tijdslot,
                                    overzicht_medewerkers=overzicht_medewerkers)
            else:
                return render_template("login_error.html")
    else:
        return render_template("login_error.html")

@bp_rooster.route('/aanpassen/submit', methods=["POST"])
def update_rooster_tabel():
    rooster = request.form['rooster_tabel']
    data  = json.loads(rooster)
    # print(data)

    for rij in data:
        voornaam = rij[0]
        achternaam = rij[1]
        medewerker = db.session.query(medewerker_models.Medewerker).filter(medewerker_models.Medewerker.voornaam == voornaam, medewerker_models.Medewerker.achternaam == achternaam).first()

        tijdslot_omschrijving = rij[2]
        tijdslot = db.session.query(medewerker_models.Tijdslot).filter(medewerker_models.Tijdslot.omschrijving == tijdslot_omschrijving).first()

        dag = rij[3]
        beschikbaarheid_code = rij[4]
        db.session.query(medewerker_models.Werkrooster).filter(medewerker_models.Werkrooster.medewerker_id==medewerker.id, medewerker_models.Werkrooster.tijdslot_id==tijdslot.id, medewerker_models.Werkrooster.dag==dag).update({medewerker_models.Werkrooster.beschikbaarheid_code:beschikbaarheid_code}, synchronize_session = False)
    
    db.session.commit()

    rooster = medewerker_models.Werkrooster.query.all()
    overzicht_tijdslot = medewerker_models.Tijdslot.query.all()
    overzicht_medewerkers = medewerker_models.Medewerker.query.all()
    return render_template('rooster.html',
                            title='Rooster aanpassen',
                            year=datetime.now().year,
                            message='',
                            rooster=rooster,
                            overzicht_tijdslot=overzicht_tijdslot,
                            overzicht_medewerkers=overzicht_medewerkers)