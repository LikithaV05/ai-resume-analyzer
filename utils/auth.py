import json

USER_DB = "data/users.json"

def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)["users"]

def verify_user(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None
