from colorama import Fore

NOT_ENOUGH_CARDS = f"{Fore.RED}Not enough cards for supplied settings, some players might have more cards than others.{Fore.RESET}"
NOT_ENOUGH_CARDS_PER_PLAYER = (
    f"{Fore.RED}Not enough cards per player, please use at least 2 cards.{Fore.RESET}"
)
INVALID_NUMBER_CHOICE = f"{Fore.RED}Invalid number.{Fore.RESET}"
INVALID_PLAYER_AMOUNT = f"{Fore.RED}Not enough players.{Fore.RESET}"
