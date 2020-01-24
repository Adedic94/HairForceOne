from flask import Blueprint, render_template
from hf1.models import diensten_models, medewerker_models
from hf1.database import db
from datetime import datetime

bp_reserveren_poc = Blueprint('bp_reserveren_poc', __name__, url_prefix='/reserveren_poc',
                          template_folder='templates')


@bp_reserveren_poc.route('/')
def index():
    overzicht_medewerkers = medewerker_models.Medewerker.query.all()
    overzicht_diensten = diensten_models.Dienst.query.all()
    overzicht_tijdslot = medewerker_models.Tijdslot.query.all()
    return render_template('reserveren_poc.html',
                           title='reserveren',
                           year=datetime.now().year,
                           message='',
                           diensten=overzicht_diensten,
                           medewerkers = overzicht_medewerkers,
                           tijdslots = overzicht_tijdslot)
