from datetime import datetime
from utils.database import analysis_collection

def log_activity(email, action, details):

    analysis_collection.insert_one({
        "email": email,
        "action": action,
        "details": details,
        "time": datetime.utcnow()
    })