from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://mongodb:27017/mongotask'

mongo = PyMongo(app)
CORS(app)


# GET ALL TASKS
@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    tasks = mongo.db.tasks.find()
    result = []

    for t in tasks:
        result.append({
            '_id': str(t['_id']),
            'title': t['title']
        })

    return jsonify(result)


# ADD TASK (ONLY ONE VERSION)
@app.route('/api/task', methods=['POST'])
def add_task():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400

    task_id = mongo.db.tasks.insert_one({'title': data['title']}).inserted_id
    new_task = mongo.db.tasks.find_one({'_id': task_id})

    return jsonify({
        'result': {
            '_id': str(new_task['_id']),
            'title': new_task['title']
        }
    })


# UPDATE TASK
@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()

    mongo.db.tasks.update_one(
        {'_id': ObjectId(id)},
        {"$set": {"title": data['title']}}
    )

    updated = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    return jsonify({
        'result': {
            '_id': id,
            'title': updated['title']
        }
    })


# DELETE TASK
@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    response = mongo.db.tasks.delete_one({'_id': ObjectId(id)})

    if response.deleted_count == 1:
        return jsonify({'result': {'message': 'record deleted'}})

    return jsonify({'result': {'message': 'no record found'}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5060, debug=True)
