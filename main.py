import os
import vlc
import torch
import binascii

from utils import *
from UserDao import UserDao
from flask_cors import CORS
from base64 import b64encode
from functools import reduce
from datetime import datetime
from termcolor import colored
from flask import Flask, request, jsonify
from bcrypt import checkpw, gensalt, hashpw
from flask_login import LoginManager, UserMixin, login_user, login_required

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Set secret key
app.secret_key = binascii.b2a_hex(os.urandom(15))

user_dao = UserDao("users.db")
user_dao.create_table()

print(colored("Starting AI API..", "green"))

if torch.cuda.is_available():
    print(colored("\t=> Using GPU.", "blue"))
    device = torch.device("cuda")
else:
    print(colored("\t=> Using CPU (Wrapper API).", "blue"))
    device = torch.device("cpu")

MODELS = ("v1", "v2", "v2-beta", "v3", "lexica", "prodia")


# Configure user_loader function to load user objects
@login_manager.user_loader
def load_user(user_id):
    print(colored("Loading user..", "green"))
    user = user_dao.get_user_by_id(int(user_id))
    return User(user[0]) if user else None


# Create a User class that extends UserMixin
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


# Show all available endpoints
@app.route("/help", methods=["GET"])
def help():
    return open("static/help.html", "r", encoding="utf-8").read(), 200


# Create a new user
@app.route("/user", methods=["POST"])
def create_user():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        created_at = str(datetime.now())
        api_key = data["api_key"]

        if username is None or password is None or api_key is None:
            return jsonify({"message": "Missing parameters"}), 400

        user = user_dao.get_user_by_username(username)
        if user:
            return jsonify({"message": "User already exists"}), 400

        user_id = user_dao.insert_user(
            username, hashpw(password.encode("utf-8"), gensalt()), created_at, api_key
        )

        # Log in the newly created user
        user = User(user_id)
        login_user(user)

        return jsonify({"message": "User created"}), 201
    else:
        return jsonify({"message": "Method not allowed"}), 405


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        if username is None or password is None:
            return jsonify({"message": "Missing parameters"}), 400

        user = user_dao.get_user_by_username(username)
        if not user or not checkpw(password.encode("utf-8"), user[2]):
            return jsonify({"message": "Invalid credentials"}), 401

        # Log in the user
        user = User(user[0])
        login_user(user)

        return jsonify({"message": "User logged in"}), 200
    else:
        return jsonify({"message": "Method not allowed"}), 405


# Generate an image from a prompt with given model
@app.route("/text2img", methods=["POST"])
@login_required
def text2img():
    try:
        data = request.get_json()
        prompt = data["prompt"]
        model = data["model"]

        if prompt is None or model is None:
            return jsonify({"success": False, "message": "Missing parameters"}), 400

        if model not in MODELS:
            return jsonify({"success": False, "message": "Invalid model"}), 400

        # Generate image
        image_url = generate_image(prompt, model)

        if image_data:
            # Encode image data in base64
            image_data = b64encode(image_data).decode("utf-8")
            return jsonify({"success": True, "image": image_url}), 200
    except Exception as e:
        print(colored("Error generating image:", "red"), e)
        return jsonify({"success": False, "message": "Error generating image"}), 500


# Greet the user
@app.route("/greet", methods=["GET"])
@login_required
def greet_user():
    try:
        name = request.args.get("name")

        if name is None:
            return jsonify({"success": False, "message": "Missing parameters"}), 400

        # Greet the user
        greeting = greet
        greeting = greeting(name)

        if greeting:
            return jsonify({"success": True, "greeting": greeting}), 200
    except Exception as e:
        print(colored("Error greeting user:", "red"), e)
        return jsonify({"success": False, "message": "Error greeting user"}), 500


# Query the AI Chatbot
@app.route("/text", methods=["POST"])
@login_required
def chat():
    try:
        data = request.get_json()
        prompt = data["prompt"]

        if prompt is None:
            return jsonify({"success": False, "message": "Missing parameters"}), 400

        # Response text
        reply = query_chatbot(prompt, print_prompt)

        if reply:
            return jsonify({"success": True, "text": reply}), 200
    except Exception as e:
        print(colored("Error generating image:", "red"), e)
        return jsonify({"success": False, "message": "Error generating image"}), 500


# Play sawtu safiri al bulbuli
@app.route("/sawtu", methods=["GET"])
def lol():
    # Use lambda
    play_sound = lambda: vlc.MediaPlayer("lol.mp3").play()

    # Play sound
    play_sound()

    return jsonify({"success": True, "message": "Sawtu safiri al bulbuli"}), 200


# Accept two lists and send it back as one list, using a lambda function that takes the two lists as arguments
@app.route("/sum", methods=["POST"])
def sum():
    try:
        data = request.get_json()
        list1 = data["list1"]
        list2 = data["list2"]

        if list1 is None or list2 is None:
            return jsonify({"success": False, "message": "Missing parameters"}), 400

        # Sum the two lists
        sum = lambda list1, list2: list1 + list2
        sum = sum(list1, list2)

        if sum:
            return jsonify({"success": True, "sum": sum}), 200
    except Exception as e:
        print(colored("Error summing lists:", "red"), e)
        return jsonify({"success": False, "message": "Error summing lists"}), 500

# Beispiel-Funktionen
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

# Hauptfunktion, die je nach übergebenem Operator andere Funktionen aufruft
def calculate(operation, a, b):
    if operation == 'add':
        return add(a, b)
    elif operation == 'subtract':
        return subtract(a, b)
    elif operation == 'multiply':
        return multiply(a, b)
    else:
        return "Invalid operation"

# Flask-Route, die die Hauptfunktion aufruft
@app.route('/calculate', methods=['POST'])
def calculate_endpoint():
    data = request.json
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')

    result = calculate(operation, a, b)
    return f"Result: {result}"

@app.route("/sort_list", methods=["GET"])
def sort_list():
    data = request.get_json()
    list_to_sort = data["list_to_sort"]

    # Sort the list using lambda functions and custom sorting
    sort_list = lambda list: sorted(list, key=lambda x: x[1])

    # Sort the list
    sorted_list = sort_list(list_to_sort)

    return jsonify({"success": True, "sorted_list": sorted_list}), 200


@app.route("/f_demo", methods=["GET"])
def f_demo():
    data = request.get_json()
    list_to_filter = data["list_to_filter"]

    # Filter the list using lambda functions and custom filtering
    filter_list = lambda list: list(filter(lambda x: x[1] > 2, list))

    # Filter the list
    filtered_list = filter_list(list_to_filter)

    return jsonify({"success": True, "filtered_list": filtered_list}), 200


@app.route("/m_demo", methods=["GET"])
def m_demo():
    data = request.get_json()
    list_to_map = data["list_to_map"]

    # Map the list using lambda functions and custom mapping
    map_list = lambda list: list(map(lambda x: x[1] * 2, list))

    # Map the list
    mapped_list = map_list(list_to_map)

    return jsonify({"success": True, "mapped_list": mapped_list}), 200


@app.route("/r_demo", methods=["GET"])
def r_demo():
    data = request.get_json()
    list_to_reduce = data["list_to_reduce"]

    # Reduce the list using lambda functions and custom reducing
    reduce_list = lambda list: reduce(lambda x, y: x + y, list)

    # Reduce the list
    reduced_list = reduce_list(list_to_reduce)

    return jsonify({"success": True, "reduced_list": reduced_list}), 200


@app.route("/combined_demo", methods=["GET"])
def combined_demo():
    data = request.get_json()
    list_to_combine = data["list_to_combine"]

    # Map, filter and reduce the list using lambda functions and custom mapping, filtering and reducing
    combined_list = lambda list: reduce(
        lambda x, y: x + y, map(lambda x: x[1] * 2, filter(lambda x: x[1] > 2, list))
    )

    # Combine the list
    combined_list = combined_list(list_to_combine)

    return jsonify({"success": True, "combined_list": combined_list}), 200


@app.route("/combined_demo2", methods=["GET"])
def transform_and_aggregate_lists():
    data = request.get_json()
    list_to_combine = data["list_to_combine"]

    # Map, filter and reduce the list using lambda functions and custom mapping, filtering and reducing
    combined_list = lambda list: reduce(
        lambda x, y: x + y, map(lambda x: x[1] * 2, filter(lambda x: x[1] > 2, list))
    )

    # Combine the list
    combined_list = combined_list(list_to_combine)

    return jsonify({"success": True, "combined_list": combined_list}), 200


# Return all models
@app.route("/models", methods=["GET"])
def models():
    return jsonify({"models": MODELS}), 200


if __name__ == "__main__":
    app.run()
