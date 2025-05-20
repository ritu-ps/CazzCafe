from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# File to store messages
MESSAGES_FILE = 'messages.json'

# File to store orders
ORDERS_FILE = 'orders.json'

@app.route('/')
def serve_html():
    return send_from_directory('.', 'coffee.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        print('Received data:', data)  # Debug print
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        # Read existing messages
        with open(MESSAGES_FILE, 'r') as f:
            messages = json.load(f)
        
        # Add timestamp to message
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages.append(data)
        
        # Save updated messages
        with open(MESSAGES_FILE, 'w') as f:
            json.dump(messages, f, indent=2)
            
        return jsonify({'message': 'Message received successfully!'}), 200
    except Exception as e:
        print('Error:', str(e))  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET'])
def get_messages():
    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)
    return jsonify(messages)

@app.route('/api/order', methods=['POST'])
def handle_order():
    try:
        data = request.get_json()
        print('Received order:', data)  # Debug print
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        # Validate order
        required_fields = ['name', 'address', 'phone', 'items']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Read existing orders
        try:
            with open(ORDERS_FILE, 'r') as f:
                orders = json.load(f)
        except FileNotFoundError:
            orders = []
        
        # Add timestamp to order
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        orders.append(data)
        
        # Save updated orders
        with open(ORDERS_FILE, 'w') as f:
            json.dump(orders, f, indent=2)
            
        return jsonify({'success': True, 'message': 'Order placed successfully!'}), 200
    except Exception as e:
        print('Error:', str(e))  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            orders = json.load(f)
        return jsonify(orders)
    except FileNotFoundError:
        return jsonify([]), 200
    except Exception as e:
        print('Error:', str(e))  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)