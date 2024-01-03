from app.db.db_teachers import query_teacher


def response_user_json(data, email_required=True, rol_required=True, id_teacher_required=True):
    required_fields = ["username", "passwd"]

    if email_required:
        required_fields.append("email")
    if rol_required:
        required_fields.append("rol")
    if id_teacher_required:
        required_fields.append("id_teacher")

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return None, f"{missing_fields[0]} is required"

    id_teacher = data["id_teacher"] if "id_teacher" in data else None

    if id_teacher is not None and query_teacher(id_teacher) is None:
        return None, "teacher not found"

    auth = {field: str(data[field]) for field in required_fields}
    auth["id_teacher"] = id_teacher

    return auth, None
