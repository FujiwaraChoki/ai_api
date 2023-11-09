import requests

from utils import *

BASE_URL = "http://127.0.0.1:5000"


def test_sawtu():
    r = requests.get(BASE_URL + "/sawtu")
    print(r.json())


test_sawtu()
