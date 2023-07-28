from requests import get


def get_cards(username: str, key: str, base_url: str) -> list[str] | str:
    response = get(f"{base_url}/held-cards", json={"username": username, "key": key})
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def get_card_pool(username: str, key: str, base_url: str) -> dict[str, list[str]] | str:
    response = get(f"{base_url}/played-cards", json={"username": username, "key": key})
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def get_player_names(base_url: str) -> list[str]:
    return get(f"{base_url}/player-names").json()


def get_played_players(username: str, key: str, base_url: str) -> list[str] | str:
    response = get(
        f"{base_url}/played-players", json={"username": username, "key": key}
    )
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def get_question(base_url: str) -> str:
    return get(f"{base_url}/active-question").text


def is_voting(base_url: str) -> bool:
    if get(f"{base_url}/is-voting").status_code == 200:
        return True
    else:
        return False
