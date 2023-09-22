import os 
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from logic import preformance_tracking

load_dotenv()

USER = os.getenv("USER")
PASS = os.getenv("PASSWORD")
CONNECTION_STRING = f"mongodb+srv://{USER}:{PASS}@cluster0.tspozkq.mongodb.net/?retryWrites=true&w=majority"


app = Flask(__name__)

client = MongoClient(CONNECTION_STRING)
db = client.main
workers = db.workers


#get all the workers with all the details
@app.route('/api/workers', methods=['GET'])
def get_workers():
    users = []
    cursor = workers.find({}, {"_id": 0})
    for worker in cursor:
        users.append(worker)
    return users


#add a worker
@app.route('/api/addworker', methods=['POST'])
def add_worker():
    worker = request.get_json()

    result = workers.insert_one(worker)
    inserted_worker = workers.find_one({"_id": result.inserted_id})

    inserted_worker['_id'] = str(inserted_worker['_id'])
    return jsonify(inserted_worker)


#get a worker details by his name
@app.route('/api/one_worker/<string:name>', methods=['GET'])
def one_worker(name :str):
    worker = workers.find_one({"worker.name": name}, {"_id": 0})
    return jsonify(worker)

#get worker performance by his name
@app.route('/api/get-worker-preformance/<string:name>', methods=['GET'])
def get_performance(name :str):
    worker = workers.find_one({"worker.name": name}, {"_id": 0})
    return preformance_tracking.worker_preformance(json.dumps(worker))

@app.route('/api/get-worker-location/<string:name>', methods=['GET'])
def get_workers_location(name :str):
    worker = workers.find_one({"worker.name": name}, {"_id": 0})
    return worker["worker"]["coordinate"]

@app.route('/api/get-workers-preformance', methods=['GET'])
def get_workers_performance():
    dict1 = {"workers":[]}
    cursor = workers.find({}, {"_id": 0})
    for worker in cursor:
        dict1["workers"].append(worker)
    return preformance_tracking.workers_preformance(json.dumps(dict1))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)