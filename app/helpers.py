def userhelper(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "password": user["password"]
    }


def todohelper(todo):
    return {
        'id': str(todo["_id"]),
        'title': str(todo['title']),
        'user_id': str(todo["user_id"])
    }
