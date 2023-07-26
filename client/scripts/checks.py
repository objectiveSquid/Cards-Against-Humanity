from requests import RequestException, get


def check_credentials(username: str, key: str, base_url: str) -> tuple[bool, str]:
    try:
        response = get(
            f"{base_url}/check-credentials",
            json={"username": username, "key": key},
        )
        return True if response.status_code == 200 else False, response.text
    except RequestException:
        return None, "CANNOT_CONNECT"
