from os import system, name
from colorama import Fore


def format_cards(cards: list[str]) -> str:
    output = ""
    for card_index, card in enumerate(cards):
        output += f"{Fore.YELLOW if card_index % 2 == 0 else Fore.MAGENTA}{card_index + 1}: {card}\n"
    return output


def clear_screen() -> None:
    if name == "nt":
        system("cls")
    else:
        system("clear")


def format_played_players(
    player_names: list[str], played_players: list[str], ignore_name: str
) -> str:
    output = ""
    for player_name in player_names:
        if player_name == ignore_name:
            continue
        if player_name not in played_players:
            output += Fore.RED
        else:
            output += Fore.GREEN
        output += player_name.title() + "\n"
    return output.removesuffix("\n")
