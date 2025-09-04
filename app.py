from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")

def connect_to_mongodb():
    return MongoClient(MONGO_URI)

@app.route("/")
def home():
    return "Hello, Mongo Insert API is running"

@app.route("/insert", methods=["POST"])
def insert_data():
    data = request.get_json()
    database_name = data.get("database")
    collection_name = data.get("collection")
    document = data.get("document")  
    if not database_name or not collection_name or not document:
        return jsonify({"status": "error", "message": "database, collection, and document are required"}), 400

    client = connect_to_mongodb()
    try:
        db = client[database_name]
        collection = db[collection_name]

        if isinstance(document, list):
            result = collection.insert_many(document)
            inserted_ids = [str(_id) for _id in result.inserted_ids]
            return jsonify({"status": "success", "inserted_ids": inserted_ids})
        else:
            result = collection.insert_one(document)
            return jsonify({"status": "success", "inserted_id": str(result.inserted_id)})
    except PyMongoError as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        client.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

