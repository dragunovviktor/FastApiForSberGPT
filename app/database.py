from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Подключение к MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]

# Коллекции
vsp_collection = db["vsp"]
object_collection = db["object"]
repair_collection = db["repair"]
maintenance_plan_collection = db["maintenance_plan"]
work_log_collection = db["work_log"]
photo_collection = db["photo"]
map_collection = db["map"]