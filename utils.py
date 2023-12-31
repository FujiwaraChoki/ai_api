import requests


def url_encode(string: str) -> str:
    """
    Encode a string to be used in a URL

    :param string: String to encode
    """
    return string.replace(" ", "%20")


def generate_image(prompt: str, model: str) -> str:
    """
    Generate an image from a prompt with given model

    :param prompt: Prompt to generate image from
    :param model: Model to use for generation
    """
    url = f"https://hercai.onrender.com/{model}/text2image?prompt={prompt}"

    r = requests.get(url)

    image_url = r.json()["url"]

    if r.status_code == 200 and image_url is not None:
        return image_url
    else:
        return None


def query_chatbot(prompt: str, print_prompt: object) -> str:
    """
    Query the AI Chatbot

    :param prompt: Prompt to query the chatbot with
    """
    print_prompt(prompt)

    url = f"https://hercai.onrender.com/v2/hercai?question={prompt}"

    r = requests.get(url)

    reply = r.json()["reply"]

    if r.status_code == 200 and reply is not None:
        return reply
    else:
        return None

def greet(name: str) -> str:
    """
    Greet a user

    :param name: Name of the user to greet
    """
    return f"Hello, {name}! I am your personal AI assistant. Start by visitng /help."

def print_prompt(prompt: str) -> str:
    """
    Prints the prompt

    :param prompt: Prompt to print
    """
    print(prompt)