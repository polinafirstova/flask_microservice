from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description} for item in items])

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Name is required'}), 400
    item = Item(name=data['name'], description=data.get('description'))
    db.session.add(item)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'Conflict', 'message': 'Item already exists'}), 409
    return jsonify({'id': item.id, 'name': item.name}), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Not Found', 'message': 'Item does not exist'}), 404
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Not Found', 'message': 'Item does not exist'}), 404

    data = request.get_json()
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']

    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description}), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Not Found', 'message': 'Item does not exist'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
