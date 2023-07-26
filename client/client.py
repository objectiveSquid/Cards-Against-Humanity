from scripts.msgs import VALID_CREDENTIALS, CURRENT_QUESTION, CHOOSE_CARD, YOUR_CARDS
from scripts.fetch import get_card_pool, get_question, is_voting, get_cards
from scripts.warns import INVALID_CREDENTIALS, GENERIC_ERROR
from scripts.visual import format_cards, clear_screen
from scripts.alternatives import string_format
from scripts.checks import check_credentials
from scripts.user_input import getch_int
from scripts.get_login import get_login
from scripts.send import submit_cards
from time import sleep

SCHEME = "http"
HOST = "127.0.0.1"
PORT = "80"


def main() -> None:
    LOGIN = get_login()
    USERNAME = LOGIN["username"]
    KEY = LOGIN["key"]
    BASE_URL = f"{SCHEME}://{HOST}:{PORT}"

    valid_credentials_check = check_credentials(USERNAME, KEY, BASE_URL)
    if not valid_credentials_check[0]:
        print(INVALID_CREDENTIALS + valid_credentials_check[1])
        exit()
    else:
        print(VALID_CREDENTIALS)

    try:  # im sorry for - i have sinned mr. "good design"
        while True:
            clear_screen()
            question = get_question(USERNAME, KEY, BASE_URL)
            voting = is_voting(USERNAME, KEY, BASE_URL)
            chosen_cards = []
            if voting:
                card_pool = get_card_pool(USERNAME, KEY, BASE_URL)
                # TODO
            else:
                held_cards = get_cards(USERNAME, KEY, BASE_URL)
                while True:
                    clear_screen()
                    print(YOUR_CARDS + format_cards(held_cards))
                    print(CURRENT_QUESTION + string_format(question, chosen_cards))
                    print(CHOOSE_CARD, end="", flush=True)
                    chosen_card_index = getch_int(
                        1, len(held_cards), other_allowed="cs"
                    )
                    if chosen_card_index == "c":
                        held_cards.extend(chosen_cards)
                        chosen_cards.clear()
                        continue
                    elif chosen_card_index == "s":
                        cards_submit_response = submit_cards(
                            USERNAME, KEY, chosen_cards, BASE_URL
                        )
                        if not cards_submit_response[0]:
                            print(GENERIC_ERROR + cards_submit_response[1])

                    else:
                        chosen_cards.append(held_cards.pop(chosen_card_index - 1))
    except Exception as error:
        print(error)
        exit()
    except KeyboardInterrupt:
        print("Exiting...")
        sleep(1)
        exit()


if __name__ == "__main__":
    main()
