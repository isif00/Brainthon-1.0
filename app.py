import os 
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

USER = os.getenv("USER")
PASS = os.getenv("PASSWORD")
CONNECTION_STRING = f"mongodb+srv://{USER}:{PASS}@cluster0.tspozkq.mongodb.net/?retryWrites=true&w=majority"


app = Flask(__name__)

client = MongoClient(CONNECTION_STRING)
db = client.main
workers = db.workers

users = []
@app.route('/api/workers', methods=['GET'])
def get_workers():
    cursor = workers.find({}, {"_id": 0})
    for worker in cursor:
        users.append(worker)
    
    return users


@app.route('/api/addworker', methods=['POST'])
def add_worker():
    worker = request.get_json()

    result = workers.insert_one(worker)
    inserted_worker = workers.find_one({"_id": result.inserted_id})

    inserted_worker['_id'] = str(inserted_worker['_id'])
    return jsonify(inserted_worker)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)