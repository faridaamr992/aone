from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/greet', methods=['POST'])
def greet():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    if data['message'].lower() == 'hello':
        return jsonify({'response': 'Hello Farida'}), 200
    else:
        return jsonify({'response': 'I only respond to "hello".'}), 200

if __name__ == '__main__':
    app.run(debug=True)
