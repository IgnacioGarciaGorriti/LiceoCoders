from flask import Blueprint, make_response
from flask_login import login_required

from models.user import user_list, get_user

users = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')


@users.get('/')
@login_required
def get_users():
    list_users = [user.to_json('list') for user in user_list]

    return make_response(list_users, 200)


@users.get('/<id>')
@login_required
def user_show(id):
    try:
        user = get_user(id)

        return make_response(user, 200)
    except Exception as e:
        return make_response(e.__str__(), 400)
