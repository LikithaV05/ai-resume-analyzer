from pymongo import MongoClient

MONGO_URI = "mongodb+srv://likithav8050_db_user:likithav1234@cluster0.vftfdtx.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)

db = client["resume_analyzer"]

login_collection = db["logins"]
analysis_collection = db["analysis"]