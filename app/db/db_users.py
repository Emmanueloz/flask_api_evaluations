from app.db.connection import db
from app.models.md_users import Users
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


def add_user(data: dict):

    passwd_hash = generate_password_hash(data["passwd"])

    new_user: Users = Users(data["username"], data["email"],
                            passwd_hash, data["rol"], data["id_teacher"])
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_json(), None
    except IntegrityError as e:
        print(e)
        return None, "Integrity error when adding username or mail already exists"
    except Exception as e:
        print((e))
        return None, "Error when adding the user"


def query_user(username):
    try:
        user: Users = Users.query.get(username)
        if user is None:
            return None, "user not found"
        return user, None
    except Exception as e:
        print(e)
        return None, "Error when adding the user"


def query_all_users(page, limit):
    result = Users.query.paginate(page=page, per_page=limit)
    users: list[Users] = result.items
    items = [item.to_json() for item in users]
    length = len(items)
    return items, length


def update_teacher(id: str, data: dict):
    try:
        teacher, error = query_user(id)
        if error is not None:
            return None, error

        if teacher.username == "admin" and data["username"] != "admin":
            return None, "You can't update the admin user"

        passwd_hash = generate_password_hash(data["passwd"])

        teacher.username = data["username"]
        teacher.email = data["email"]
        teacher.passwd = passwd_hash
        teacher.rol = data["rol"]
        teacher.id_teacher = data["id_teacher"]
        db.session.commit()
        return teacher, None
    except IntegrityError as e:
        print(e)
        return None, "Integrity error when adding username or mail already exists"
    except Exception as e:
        print(e)
        return None, "Error when updating the user"


def del_user(id: str):
    try:
        user, error = query_user(id)
        if error is not None:
            return None, error

        if user.username == "admin":
            return None, "You can't delete the admin user"

        db.session.delete(user)
        db.session.commit()
        return user, None
    except Exception as e:
        print(e)
        return None, "Error when deleting the user"
