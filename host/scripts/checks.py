from scripts.player import Player


def can_vote_winner(
    key: str,
    username: str,
    winner_username: str,
    vote_in_progress: bool,
    players: dict[str, Player],
) -> tuple[bool, str]:
    if not vote_in_progress:
        return False, "NO_VOTE_IN_PROGRESS"

    authenticated = auth(key, username, players)
    if not authenticated[0]:
        return False, authenticated[1]

    player = players.get(username)
    if not username_exists(winner_username):
        return False, "WINNER_USER_NOT_FOUND"
    elif player.has_voted:
        return False, "PLAYER_HAS_VOTED"

    return True, "ALL_TESTS_PASSED"


def can_see_played_cards(
    key: str,
    username: str,
    vote_in_progress: bool,
    players: dict[str, Player],
) -> tuple[bool, str]:
    authenticated = auth(key, username, players)
    if not authenticated[0]:
        return False, authenticated[1]
    elif not vote_in_progress:
        return False, "VOTE_NOT_IN_PROGRESS"

    return True, "ALL_TESTS_PASSED"


def can_play_cards(
    key: str,
    username: str,
    required_cards: int,
    card_pool: dict[str, list[str]],
    cards_to_play: list[str],
    players: dict[str, Player],
) -> tuple[bool, str]:
    authenticated = auth(key, username, players)
    if not authenticated[0]:
        return False, authenticated[1]

    player = players.get(username)
    if len(cards_to_play) != required_cards:
        return False, "INVALID_CARD_AMOUNT"
    elif len(cards_to_play) > len(player.cards):
        return False, "NOT_ENOUGH_CARDS"
    elif ["" for card in cards_to_play if card not in player.cards]:
        return False, "CARDS_NOT_OWNED_BY_PLAYER"
    elif username in card_pool:
        return False, "PLAYER_HAS_ALREADY_PLAYED_CARDS"

    return True, "ALL_TESTS_PASSED"


def username_exists(username: str, players: dict[str, Player]) -> bool:
    player = players.get(username)
    if player == None:
        return False
    return True


def auth(key: str, username: str, players: dict[str, Player]) -> tuple[bool, str]:
    if not username_exists(username, players):
        return False, "PLAYER_NOT_FOUND"

    player = players.get(username)
    if player.key != key:
        return False, "INVALID_KEY"
    return True, "SUCCESS"
