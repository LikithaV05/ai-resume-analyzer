from datetime import datetime
from utils.database import login_collection

def save_login(email):

    login_collection.insert_one({
        "email": email,
        "login_time": datetime.utcnow()
    })