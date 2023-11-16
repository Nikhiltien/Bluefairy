from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient("mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority")

# Select your database
db = client["Bluefairy"]

# Iterate over all collections in the database and drop each one
for collection_name in db.list_collection_names():
    db[collection_name].drop()

print("All documents in all collections have been deleted.")
