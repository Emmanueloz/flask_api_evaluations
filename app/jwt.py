from flask_jwt_extended import JWTManager
from app.db.db_users import query_user

jwtm = JWTManager()


@jwtm.user_identity_loader
def user_identity_lookup(user):
    return user.username


@jwtm.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # print(jwt_data)
    identity = jwt_data["sub"]
    user, error = query_user(identity)
    return user
