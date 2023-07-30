from requests import RequestException, post


def submit_cards(
    username: str, key: str, cards: list[str], base_url: str
) -> tuple[bool, str]:
    """return value: tuple[True is success - failure is False, reason for fail or success]"""
    try:
        response = post(
            f"{base_url}/play-cards",
            json={"username": username, "key": key, "cards": cards},
        )
        return True if response.status_code == 200 else False, response.text
    except RequestException:
        return False, "CANNOT_CONNECT"


def vote_winner(
    winner_name: str, username: str, key: str, base_url: str
) -> tuple[bool, str]:
    """return value: tuple[True is success - False is failure, reason for fail or success]"""
    try:
        response = post(
            f"{base_url}/vote-winner",
            json={"username": username, "key": key, "winner": winner_name},
        )
        return True if response.status_code == 200 else False, response.text
    except RequestException:
        return False, "CANNOT_CONNECT"
