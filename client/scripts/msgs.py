from colorama import Fore

ASK_USERNAME = f"{Fore.BLUE}Username: {Fore.RESET}"
ASK_KEY = f"{Fore.BLUE}Key/Password: {Fore.RESET}"
VALID_CREDENTIALS = f"{Fore.GREEN}Credentials passed.{Fore.RESET}"
YOUR_CARDS = f"{Fore.BLUE}Your cards: \n{Fore.RESET}"
CURRENT_QUESTION = f"{Fore.BLUE}Question: {Fore.RESET}"
CHOOSE_CARD = f"{Fore.BLUE}Choose a card to play, C to remove selected cards, S to sumbit answers: {Fore.RESET}"
WAIT_FOR_OTHER_PLAYERS = (
    f"{Fore.BLUE}Please wait for the other players to play their cards:{Fore.RESET}"
)
