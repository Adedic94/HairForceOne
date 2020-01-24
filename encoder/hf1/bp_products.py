from flask import Blueprint, render_template
from hf1.models import artikel_models
from hf1.database import db
from hf1.login_functie import *
from datetime import datetime

bp_products = Blueprint('bp_products', __name__, url_prefix='/products',
                        template_folder='templates')

@bp_products.route('/')
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
    # artikelgroepen = db.session.query(artikel_models.Artikelgroep).filter(artikel_models.Artikelgroep.vervallen == True).all()
    artikelgroepen = db.session.query(artikel_models.Artikel).filter(artikel_models.Artikel.artikelgroep_id == 1).all()
    return render_template('products.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen,
                           ingelogd=ingelogd)

@bp_products.route('/aanpassen')
def show_producten_edit():
    artikelgroepen = db.session.query(artikel_models.Artikelgroep).all()
    return render_template('producten_edit.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen)

@bp_products.route('/aanpassen/submit', methods=["POST"])
def update_producten_tabel():
    product = request.form['producten_tabel']
    data  = json.loads(product)
    
    artikel_models.Artikel.query.delete()
    new_id = 0
    for entry in data:
        omschrijving = entry[0]
        prijs = entry[1]
        try:
            prijs = float(prijs.replace(',', '.'))
        except ValueError:
            prijs="0.0"
            
        artikelgroep = artikel_models.Artikelgroep.query.filter_by(omschrijving=str(entry[2])).first()
        
        if artikelgroep == None:
            artikelgroep = artikel_models.Artikelgroep.query.filter_by(omschrijving='Overig').first()
        
        new_entry = artikel_models.Artikel(artikelgroep, omschrijving, prijs)

        new_entry.artikelgroep = artikelgroep
        new_entry.id =new_id
        new_id += 1
        new_entry.artikelgroep_id = artikelgroep.id #moet nog artikelgroep id fixen
        
        db.session.add(new_entry)
    db.session.commit()
    
    
    res = make_response("datainvoer test " + product)

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

    producten = artikel_models.Artikel.query.all()
    artikelgroepen = artikel_models.Artikelgroep.query.all()
    return render_template('products.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen,
                           ingelogd=ingelogd)
@bp_products.route('/shampoo')
def shampoo():
    artikelgroepen = db.session.query(artikel_models.Artikel).filter(artikel_models.Artikel.artikelgroep_id == 1).all()

    return render_template('shampoo.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen)

@bp_products.route('/conditioner')
def conditioner():
    artikelgroepen = db.session.query(artikel_models.Artikel).filter(artikel_models.Artikel.artikelgroep_id == 2).all()

    return render_template('conditioner.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen)


@bp_products.route('/spray')
def spray():
    artikelgroepen = db.session.query(artikel_models.Artikel).filter(artikel_models.Artikel.artikelgroep_id == 3).all()

    return render_template('spray.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen)

@bp_products.route('/gelwax')
def gelwax():
    artikelgroepen = db.session.query(artikel_models.Artikel).filter(artikel_models.Artikel.artikelgroep_id == 4).all()
    return render_template('gelwax.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen)

@bp_products.route('/verzorging')
def verzorging():
    artikelgroepen = db.session.query(artikel_models.Artikel).filter(artikel_models.Artikel.artikelgroep_id == 5).all()

    return render_template('verzorging.html',
                           title='Producten',
                           year=datetime.now().year,
                           message='Onze producten',
                           artikelgroepen=artikelgroepen)
