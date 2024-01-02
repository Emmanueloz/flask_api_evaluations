from app.db.connection import db
from app.models.md_users import Users
from sqlalchemy.exc import IntegrityError


def add_user(data: dict):
    new_user: Users = Users(data["username"], data["email"],
                            data["passwd"], data["rol"], data["id_teacher"])
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
