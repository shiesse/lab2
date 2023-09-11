from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# Функция для подключения к базе данных SQLite
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# API для создания клиента
@app.route('/clients', methods=['POST'])
def create_client():
    name = request.json['name']
    email = request.json['email']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO clients (name, email) VALUES (?, ?)', (name, email))
    db.commit()

    return jsonify({'message': 'Client created successfully'}), 201

# API для получения списка клиентов
@app.route('/clients', methods=['GET'])
def get_clients():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    db.close()

    clients_list = []
    for client in clients:
        clients_list.append({'id': client['id'], 'name': client['name'], 'email': client['email']})

    return jsonify(clients_list), 200

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    name = request.json['name']
    email = request.json['email']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE clients SET name=?, email=? WHERE id=?', (name, email, client_id))
    db.commit()

    return jsonify({'message': 'Client updated successfully'}), 200

# API для удаления клиента
@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM clients WHERE id=?', (client_id,))
    db.commit()

    return jsonify({'message': 'Client deleted successfully'}), 200


# API для создания услуги
@app.route('/services', methods=['POST'])
def create_service():
    name = request.json['name']
    price = request.json['price']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO services (name, price) VALUES (?, ?)', (name, price))
    db.commit()

    return jsonify({'message': 'Service created successfully'}), 201

# API для получения списка услуг
@app.route('/services', methods=['GET'])
def get_services():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM services')
    services = cursor.fetchall()
    db.close()

    services_list = []
    for service in services:
        services_list.append({'id': service['id'], 'name': service['name'], 'price': service['price']})

    return jsonify(services_list), 200

# API для изменения услуги
@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    name = request.json['name']
    price = request.json['price']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE services SET name=?, price=? WHERE id=?', (name, price, service_id))
    db.commit()

    return jsonify({'message': 'Service updated successfully'}), 200

# API для удаления услуги
@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM services WHERE id=?', (service_id,))
    db.commit()

    return jsonify({'message': 'Service deleted successfully'}), 200


# API для создания заявки
@app.route('/requests', methods=['POST'])
def create_request():
    client_id = request.json['client_id']
    service_id = request.json['service_id']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO requests (client_id, service_id) VALUES (?, ?)', (client_id, service_id))
    db.commit()

    return jsonify({'message': 'Request created successfully'}), 201

# API для получения списка заявок
@app.route('/requests', methods=['GET'])
def get_requests():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT requests.id, clients.name as client_name, services.name as service_name FROM requests JOIN clients ON requests.client_id = clients.id JOIN services ON requests.service_id = services.id')
    requests = cursor.fetchall()
    db.close()

    requests_list = []
    for request in requests:
        requests_list.append({'id': request['id'], 'client_name': request['client_name'], 'service_name': request['service_name']})

    return jsonify(requests_list), 200

# API для изменения заявки
@app.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    client_id = request.json['client_id']
    service_id = request.json['service_id']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE requests SET client_id=?, service_id=? WHERE id=?', (client_id, service_id, request_id))
    db.commit()

    return jsonify({'message': 'Request updated successfully'}), 200

# API для удаления заявки
@app.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM requests WHERE id=?', (request_id,))
    db.commit()

    return jsonify({'message': 'Request deleted successfully'}), 200


if __name__ == '__main__':
    app.run()
