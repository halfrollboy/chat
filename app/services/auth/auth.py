import requests


def get_auth():
    res = requests.get("http://auth:8080/users/me/")
    print(res)
