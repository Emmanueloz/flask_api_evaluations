def response_teacher_json(data):
    if "name" not in data or "subject" not in data:
        return None, "name and subject required"

    teacher = {
        "name": data["name"],
        "subject": data["subject"]
    }
    return teacher, None
