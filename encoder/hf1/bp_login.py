from flask import *

from hf1.database import db
from hf1 import login_functie
from sqlalchemy.testing.pickleable import User
from werkzeug.utils import redirect

bp_login = Blueprint('bp_login', __name__, url_prefix='/login',
                     template_folder='templates')


@bp_login.route('/', methods=['GET', 'POST'])
def login_user():
    from hf1 import login_functie
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        if login_functie.login(username, password):
            res = make_response(redirect(url_for('bp_main.home')))
            id = login_functie.get_user_id(username)
            res.set_cookie('user_id', str(id), max_age=60 * 60 * 24 * 365 * 2)
            return res
        else:
            return render_template('login_no_match.html')
    return render_template('login.html')
    

@bp_login.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('user_id', 'remove', max_age=0)
    res = make_response(render_template('login_logged_out.html'))
    session.clear()
    return res

# def cookie():
#     if not request.cookies.get('foo'):
#         res = make_response("Setting a cookie")
#         res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
#     else:
#         res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
#     return res