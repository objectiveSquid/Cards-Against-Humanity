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
        output += f"{player_name.title()}{Fore.RESET}\n"
    return output.removesuffix("\n")


def format_played_cards(card_pool: dict[str, list[str]]) -> str:
    output = ""
    for played_card_index, (player_name, played_cards) in enumerate(
        zip(card_pool.keys(), card_pool.values())
    ):
        output += f"{Fore.YELLOW if played_card_index % 2 == 0 else Fore.MAGENTA}{player_name.title()}{Fore.BLUE}: {f'{Fore.RESET}, {Fore.BLUE}'.join(played_cards)}{Fore.RESET}\n"

    return output.removesuffix("\n")


def format_non_voters(
    player_names: list[str], non_voters: list[str], ignore_name: str
) -> str:
    output = ""
    for player_name in player_names:
        if player_name == ignore_name:
            continue
        if player_name not in non_voters:
            output += Fore.RED
        else:
            output += Fore.GREEN
        output += f"{player_name.title()}{Fore.RESET}\n"
    return output.removesuffix("\n")
