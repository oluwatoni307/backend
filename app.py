import openai, os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from blueprint_module import blueprint



# Create application server
app = Flask(__name__)

# Register blueprint from blueprint_module
app.register_blueprint(blueprint)

# Allow external domains to access JSON data
CORS(app)


@app.route("/")
def index():
    return "hi!!!!"

if __name__ == "__main__":
    app.run(debug=True)