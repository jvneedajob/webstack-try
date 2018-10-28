import functools

from flask import Blueprint , render_template , g
from model import User

bp = Blueprint('auth',__name__)


# @auth.url_value_preprocessor
# def get_auth_owner(endpoint, values):
#     query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
#     g.auth_owner = query.first_or_404()

@bp.route('/route/')
def route():
    return u'404'