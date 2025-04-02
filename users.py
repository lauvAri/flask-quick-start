from flask import Blueprint, jsonify
from . import db


bp = Blueprint("users", __name__, url_prefix="/users")
conn = db.get_connection()

@bp.route('')
def all():
    return jsonify(conn.find_all())

@bp.route('/<int:id>')
def user(id):
    user = conn.find_user_by_id(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({
          "error": "User not found"
        }), 404