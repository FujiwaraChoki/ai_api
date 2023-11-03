import requests

from utils import *

BASE_URL = "http://127.0.0.1:5000"


def test_create_user():
    r = requests.post(
        BASE_URL + "/user",
        json={
            "username": "FujiwaraChoki",
            "password": "sami1234",
            "api_key": "test",
        },
    )

    if r.status_code == 201:
        print("User created successfully")
    else:
        print("User creation failed")


def test_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    r = requests.post(
        BASE_URL + "/login",
        json={
            "username": username,
            "password": password,
        },
    )

    if r.status_code == 200:
        print("User logged in successfully")
    else:
        print("User login failed")


def test_login():
    # Login and get the session cookie
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_response = requests.post(
        BASE_URL + "/login",
        json={
            "username": username,
            "password": password,
        },
    )

    if login_response.status_code == 200:
        print("User logged in successfully")


def test_create_image():
    url = generate_image("Extremely beautiful landscape", "v3-beta")

    data = requests.get(url).content

    if data:
        print("Image generated successfully")
        with open("image.png", "wb") as f:
            f.write(data)


def test_query_chatbot():
    text = query_chatbot("How are you?")
    if text:
        print("Chatbot replied successfully")
        print(text)
    else:
        print("Chatbot replied failed")


test_create_user()
test_login()
test_create_image()
test_query_chatbot()
