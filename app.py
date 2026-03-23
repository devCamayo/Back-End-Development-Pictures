from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria para pruebas
pictures = []
picture_id_counter = 1

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/count', methods=['GET'])
def count():
    return jsonify({"count": len(pictures)}), 200

@app.route('/pictures', methods=['GET'])
def get_pictures():
    return jsonify(pictures), 200

@app.route('/picture/<int:id>', methods=['GET'])
def get_picture(id):
    picture = next((p for p in pictures if p['id'] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"error": "Picture not found"}), 404

@app.route('/picture', methods=['POST'])
def create_picture():
    global picture_id_counter
    data = request.get_json()
    new_picture = {
        'id': picture_id_counter,
        'name': data.get('name'),
        'url': data.get('url')
    }
    pictures.append(new_picture)
    picture_id_counter += 1
    return jsonify(new_picture), 201

@app.route('/picture/<int:id>', methods=['PUT'])
def update_picture(id):
    picture = next((p for p in pictures if p['id'] == id), None)
    if picture:
        data = request.get_json()
        picture['name'] = data.get('name', picture['name'])
        picture['url'] = data.get('url', picture['url'])
        return jsonify(picture), 200
    return jsonify({"error": "Picture not found"}), 404

@app.route('/picture/<int:id>', methods=['DELETE'])
def delete_picture(id):
    global pictures
    picture = next((p for p in pictures if p['id'] == id), None)
    if picture:
        pictures = [p for p in pictures if p['id'] != id]
        return jsonify({"message": "Picture deleted"}), 200
    return jsonify({"error": "Picture not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)