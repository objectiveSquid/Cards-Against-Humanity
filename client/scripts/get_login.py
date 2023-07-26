from scripts.warns import *
from scripts.msgs import *


def get_username() -> str:
    username = input(ASK_USERNAME).strip().lower()
    if len(username) == 0:
        print(INVALID_USERNAME)
        return get_username()
    return username


def get_key() -> str:
    password = input(ASK_KEY)
    if len(password) == 0:
        print(INVALID_KEY)
        return get_key()
    return password


def get_login() -> dict[str, str]:
    return {"username": get_username(), "key": get_key()}
