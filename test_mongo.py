import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get URI from .env
MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_URI not found in .env")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["image_api_db"]  # you can choose any DB name
collection = db["user_names"]

# Insert a test record
result = collection.insert_one({"name": "Compass Test"})
print(f"Inserted ID: {result.inserted_id}")

# Show all documents
for doc in collection.find():
    print(doc)
