from flask import Blueprint, render_template
from hf1.models import orderoverzicht_models
from hf1.database import db
from datetime import datetime

bp_orderoverzicht = Blueprint('bp_orderoverzicht', __name__, url_prefix='/orderoverzicht',
                        template_folder='templates')


@bp_orderoverzicht.route('/')
def index():
    overzicht = orderoverzicht_models.Orderoverzicht.query.all()
    return render_template('orderoverzicht.html',
                           title='orderoverzicht',
                           year=datetime.now().year,
                           message='',
                           order=overzicht)
