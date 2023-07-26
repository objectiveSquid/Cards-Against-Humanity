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
