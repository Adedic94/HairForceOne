from flask import *
from sqlalchemy import *
from hf1.database import db
from sqlalchemy import literal

def user_exists(username):
    from hf1.models import account_models
    user = db.session.query(account_models.Account).filter(account_models.Account.email == username)
    if db.session.query(literal(True)).filter(user.exists()).scalar():
        return True
    else:
        return False

def get_user_id(username):
    try:
        from hf1.models import account_models
        user = db.session.query(account_models.Account).filter_by(email=username).first()
        # print(int(user.id))
        return int(user.id)
    except:
        return None

def check_password(user_id, password):
    if password == "password":
        return True

def check_user_role(user_id):
    from hf1.models import account_models
    user = db.session.query(account_models.Account).filter_by(id=user_id).first()
    # print(str(user.user_role))
    return str(user.user_role)

def user_is_manager(user_id):
    if check_user_role(user_id) == "manager":
        return True
    else:
        return False

def user_is_medewerker(user_id):
    if check_user_role(user_id) == "medewerker":
        return True
    else:
        return False

def logged_in():
    if not has_cookie('session'):
        return False
    else:
        return True

def login(username, password):
    if user_exists(username):
        if check_password(get_user_id(username), password):
            session["id"] = get_user_id(username)
            return True
    else:
        return False
            

def has_cookie(cookie_name):
    if not request.cookies.get(cookie_name):
        return False
    else:
        return True