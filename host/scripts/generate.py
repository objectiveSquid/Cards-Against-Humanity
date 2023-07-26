from scripts.randomness import choose_random_card
from scripts.warns import NOT_ENOUGH_CARDS
from scripts.player import Player
from random import randint


def generate_players(
    player_names: list[str], cards: list[str], cards_per_player: int = 10
) -> dict[str, Player]:
    players: list[Player] = [Player(player_name) for player_name in player_names]

    try:
        for _ in range(cards_per_player):
            for player in players:
                player.give_new_card(choose_random_card(cards))
    except ValueError:
        print(NOT_ENOUGH_CARDS)

    output_dict = {}
    for player in players:
        output_dict[player.name.lower()] = player

    return output_dict
