from requests import get


def get_cards(username: str, key: str, base_url: str) -> list[str]:
    return get(f"{base_url}/held-cards", json={"username": username, "key": key}).json()


def get_card_pool(username: str, key: str, base_url: str) -> dict[str, list[str]]:
    return get(
        f"{base_url}/played-cards", json={"username": username, "key": key}
    ).json()


def get_question(username: str, key: str, base_url: str) -> str:
    return get(
        f"{base_url}/active-question", json={"username": username, "key": key}
    ).text


def is_voting(username: str, key: str, base_url: str) -> bool:
    if (
        get(
            f"{base_url}/is-voting", json={"username": username, "key": key}
        ).status_code
        == 200
    ):
        return True
    else:
        return False
