from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/greet', methods=['POST'])
def greet():
    """
    Greet a user
    ---
    tags:
      - Greeting
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Farida
    responses:
      200:
        description: A greeting message
        schema:
          type: object
          properties:
            message:
              type: string
              example: Hello Farida
    """
    data = request.get_json()
    name = data.get("name", "Guest")
    return jsonify({"message": f"Hello {name}"})

if __name__ == '__main__':
    app.run(debug=True)
