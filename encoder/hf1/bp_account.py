from flask import Blueprint, render_template, request
from hf1.models import account_models
from hf1.database import db

bp_account = Blueprint('bp_account', __name__, url_prefix='/account',
                       template_folder='templates')


@bp_account.route('/aanmaken')
def maak_account():
    return render_template('maak_een_account_aan.html',
                           title='Registreren',
                           voornaam='',
                           achternaam='',
                           straatnaam='',
                           huisnummer='',
                           postcode='',
                           woonplaats='',
                           email='',
                           telefoon='')


@bp_account.route('/aanmaken', methods=["POST"])
def post_maak_account():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    straatnaam = request.form['straatnaam']
    huisnummer = request.form['huisnummer']
    postcode = request.form['postcode']
    woonplaats = request.form['woonplaats'] 
    email = request.form['email']
    telefoon = request.form['telefoon']
    password = request.form['password']

    errors = []
    if len(voornaam) < 1:
        errors.append("Voornaam is niet ingevuld")
    if len(achternaam) < 1:
        errors.append("Achternaam is niet ingevuld")
    if len(straatnaam) < 2:
        errors.append("Straatnaam is niet ingevuld")
    if len(huisnummer) < 1:
        errors.append("Huisnummer is niet ingevuld")
    if len(postcode) < 6:
        errors.append("Postcode is niet ingevuld")
    if len(woonplaats) < 1:
        errors.append("Woonplaats is niet ingevuld")
    if len(telefoon) < 5:
        errors.append("Telefoonnummer is niet ingevuld")
    if len(password) < 5:
        errors.append("Wachtwoord is te kort")
    if len(email) < 1:
        errors.append("E-mailadres is verpicht")
    if voornaam.lower() == 'rudi':
        errors.append("Deze persoon komt er niet in!")

    exising_account = account_models.Account.query.filter_by(
        email=email).first()
    if exising_account:
        errors.append("E-mailadres '%s' is al in gebruik." % email)

    if len(errors) == 0:
        try:
            db.session.add(account_models.Account(
                voornaam, achternaam, straatnaam, huisnummer,postcode, woonplaats, email, telefoon, "klant"))
            db.session.commit()
        except:
            errors.append("Opslaan is niet gelukt!")

    if len(errors) == 0:
        return render_template('bedankt.html')

    return render_template('maak_een_account_aan.html',
                           title='Registreren',
                           voornaam=voornaam,
                           achternaam=achternaam,
                           email=email,
                           telefoon=telefoon,
                           straatnaam=straatnaam,
                           huisnummer=huisnummer,
                           postcode=postcode,
                           woonplaats=woonplaats,
                           errors=errors)
