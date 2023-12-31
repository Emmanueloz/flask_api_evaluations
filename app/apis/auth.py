from flask import Blueprint, request, jsonify
from app.db.db_users import add_user
from app.db.db_teachers import query_teacher
from werkzeug.security import check_password_hash, generate_password_hash
bp = Blueprint("AuthApi", __name__, url_prefix="/api/auth")


def response_user_json(data):
    if "username" not in data or "email" not in data or "passwd" not in data or "rol" not in data:
        return None, "username, email, password and rol required"

    id_teacher = data["id_teacher"] if "id_teacher" in data else None

    if id_teacher is not None and query_teacher(id_teacher) is None:
        return None, "teacher not found"

    auth = {
        "username": data["username"],
        "email": data["email"],
        "passwd": data["passwd"],
        "rol": data["rol"],
        "id_teacher": id_teacher
    }
    return auth, None


@bp.post("/signup")
def sign_up():
    data = request.get_json()
    user, error = response_user_json(data)
    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 404

    passwd_hash = generate_password_hash(str(user["passwd"]))

    user["passwd"] = passwd_hash

    response, error = add_user(user)

    if error is not None:
        return jsonify({"status": "error", "action": "add", "msg": error}), 500

    return jsonify({"status": "ok", "action": "add", "length": "1", "response": response})
