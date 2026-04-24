from flask import Flask, request, jsonify, send_from_directory
import json, os

app = Flask(__name__, static_folder='static', template_folder='templates')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'encon_data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# Serve the dashboard
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

# GET all saved data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

# POST save data (full overwrite per month key)
@app.route('/api/data', methods=['POST'])
def post_data():
    body = request.get_json()
    if not body:
        return jsonify({'ok': False, 'error': 'No data'}), 400
    current = load_data()
    # Merge incoming keys into existing data
    for key, val in body.items():
        current[key] = val
    save_data(current)
    return jsonify({'ok': True, 'keys': list(current.keys())})

# DELETE a month
@app.route('/api/data/<key>', methods=['DELETE'])
def delete_month(key):
    current = load_data()
    if key in current:
        del current[key]
        save_data(current)
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
