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
    print(result.__dict__)
    users: list[Users] = result.items
    items = [item.to_json() for item in users]
    length = len(items)
    return items, length
