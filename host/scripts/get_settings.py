from scripts.warns import (
    NOT_ENOUGH_CARDS_PER_PLAYER,
    INVALID_PLAYER_AMOUNT,
    INVALID_NUMBER_CHOICE,
)
from scripts.msgs import ASK_CARDS_PER_PLAYER, ASK_PLAYER_NAMES


def get_player_names() -> list[str]:
    player_names = list(
        dict.fromkeys(
            [player_name.strip() for player_name in input(ASK_PLAYER_NAMES).split(",")]
        )
    )
    if len(player_names) < 2:
        print(INVALID_PLAYER_AMOUNT)
        return get_player_names()
    return player_names


def get_cards_per_player() -> int:
    try:
        cards_per_player = int(input(ASK_CARDS_PER_PLAYER))
    except ValueError:
        print(INVALID_NUMBER_CHOICE)
        return get_cards_per_player()
    else:
        if cards_per_player < 2:
            print(NOT_ENOUGH_CARDS_PER_PLAYER)
            return get_cards_per_player()
    return cards_per_player


def get_settings() -> dict[str, str]:
    return {
        "player_names": get_player_names(),
        "cards_per_player": get_cards_per_player(),
    }
