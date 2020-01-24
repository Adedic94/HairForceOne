from flask import Blueprint, render_template
from hf1.models import account_models, diensten_models, medewerker_models, reserveringen_models
from hf1.database import db
from datetime import datetime
from hf1.login_functie import *
# from hf1 import is_ingelogd



bp_reserveringen_overzicht = Blueprint('bp_reserveringen_overzicht', __name__, url_prefix='/reserveringen_overzicht',
                          template_folder='templates')


@bp_reserveringen_overzicht.route('/')
def index():
    if has_cookie('user_id'):
        if not logged_in():
            return render_template("login_error.html")
        else:
            if user_is_manager(session["id"]) or user_is_medewerker(session["id"]):
                overzicht_reserveringen = reserveringen_models.Reservering.query.all()
                overzicht_klanten = account_models.Account.query.all()
                overzicht_medewerkers = medewerker_models.Medewerker.query.all()
                overzicht_tijdslot = medewerker_models.Tijdslot.query.all()
                overzicht_diensten = diensten_models.Dienst.query.all()
                return render_template('reserveringen_overzicht.html',
                           title='Reserveringen Overzicht',
                           year=datetime.now().year,
                           message='',
                           overzicht_klanten = overzicht_klanten,
                           overzicht_medewerkers = overzicht_medewerkers,
                           overzicht_tijdslot= overzicht_tijdslot,
                           reserveringen_overzicht =overzicht_reserveringen,
                           overzicht_diensten = overzicht_diensten)
            else:
                return render_template("login_error.html")
    else:
        return render_template("login_error.html")

 