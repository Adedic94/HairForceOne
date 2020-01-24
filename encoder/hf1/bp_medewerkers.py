from flask import Blueprint, render_template
from hf1.models import medewerker_models
from hf1.database import db
from datetime import datetime

bp_medewerkers = Blueprint('bp_medewerkers', __name__, url_prefix='/medewerkers',
                        template_folder='templates')


@bp_medewerkers.route('/')
def index():
    medewerkers = medewerker_models.Medewerker.query.all()
    return render_template('medewerkers.html',
                           title='Onze medewerkers',
                           year=datetime.now().year,
                           message='',
                           medewerkers=medewerkers)
