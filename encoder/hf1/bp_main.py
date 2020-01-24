from flask import Blueprint, render_template
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from hf1.models import reserveringen_models, diensten_models, medewerker_models, account_models
from hf1.login_functie import *
from datetime import datetime

bp_main = Blueprint('bp_main', __name__,
                    template_folder='templates')


@bp_main.route('/')
def home():
    ingelogd = False
    mod = False
    if has_cookie('user_id'):
        if not logged_in():
            ingelogd = False
            mod = False
        else:
            ingelogd = True
            if user_is_manager(session["id"]) or user_is_medewerker(session["id"]):
                mod = True
            else:
                mod = False
    else:
        ingelogd = False

    return render_template('index.html',
                            mod= mod,
                           ingelogd=ingelogd)


@bp_main.route('/contact')
def contact():
    return render_template('contact.html',
                           title='Contact',
                           message='Waar u ons kunt vinden')


@bp_main.route('/about')
def about():
    return render_template('about.html')


@bp_main.route('/login')
def login():
    return render_template('login.html')