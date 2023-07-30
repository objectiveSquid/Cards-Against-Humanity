from scripts.msgs import (
    WAIT_FOR_OTHER_PLAYERS,
    VALID_CREDENTIALS,
    CURRENT_QUESTION,
    PLAYED_CARDS,
    CHOOSE_CARD,
    YOUR_CARDS,
    NON_VOTERS,
)
from scripts.fetch import (
    get_played_players,
    get_player_names,
    get_non_voters,
    get_card_pool,
    get_question,
    is_voting,
    get_cards,
)
from scripts.visual import (
    format_played_players,
    format_played_cards,
    format_non_voters,
    format_cards,
    clear_screen,
)
from scripts.warns import INVALID_CREDENTIALS, GENERIC_ERROR
from scripts.user_input import get_winner_name, getch_int
from scripts.send import submit_cards, vote_winner
from scripts.alternatives import string_format
from scripts.checks import check_credentials
from scripts.get_login import get_login
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
        has_played_cards = False
        has_voted = False
        PLAYER_NAMES = get_player_names(BASE_URL)
        while True:
            clear_screen()
            question = get_question(BASE_URL)
            voting = is_voting(BASE_URL)
            chosen_cards = []
            if voting and has_voted:
                non_voters_response = get_non_voters(USERNAME, KEY, BASE_URL)
                if isinstance(non_voters_response, str):
                    print(GENERIC_ERROR + non_voters_response)
                    sleep(1)
                    continue
                print(NON_VOTERS)
                print(format_non_voters(PLAYER_NAMES, non_voters_response, USERNAME))
                sleep(1)
                continue
            if voting:
                card_pool = get_card_pool(USERNAME, KEY, BASE_URL)
                if isinstance(card_pool, str):
                    print(GENERIC_ERROR + card_pool)
                    sleep(1)
                    continue
                print(PLAYED_CARDS)
                print(format_played_cards(card_pool))
                winner_name = get_winner_name(PLAYER_NAMES)
                vote_winner_response = vote_winner(winner_name, USERNAME, KEY, BASE_URL)
                if not vote_winner_response[0]:
                    print(GENERIC_ERROR + vote_winner_response[1])
                    continue
                has_voted = True
                continue
            elif has_played_cards:
                played_players_response = get_played_players(USERNAME, KEY, BASE_URL)
                if isinstance(played_players_response, str):
                    print(GENERIC_ERROR + played_players_response)
                    sleep(1)
                    continue
                print(WAIT_FOR_OTHER_PLAYERS)
                print(
                    format_played_players(
                        PLAYER_NAMES, played_players_response, USERNAME
                    )
                )
                sleep(1)
                continue
            else:
                held_cards = get_cards(USERNAME, KEY, BASE_URL)
                has_played_cards = False
                has_voted = False
                while True:
                    print(YOUR_CARDS + format_cards(held_cards))
                    print(CURRENT_QUESTION + string_format(question, *chosen_cards))
                    print(CHOOSE_CARD, end="", flush=True)
                    chosen_card_index = getch_int(
                        1, len(held_cards), other_allowed="cs"
                    )
                    if chosen_card_index == "c":
                        held_cards.extend(chosen_cards)
                        chosen_cards.clear()
                        clear_screen()
                        continue
                    elif chosen_card_index == "s":
                        cards_submit_response = submit_cards(
                            USERNAME, KEY, chosen_cards, BASE_URL
                        )
                        if not cards_submit_response[0]:
                            clear_screen()
                            print(GENERIC_ERROR + cards_submit_response[1])
                            continue
                        has_played_cards = True
                        break

                    else:
                        chosen_cards.append(held_cards.pop(chosen_card_index - 1))
                    clear_screen()
    except Exception as error:
        print(error)
        exit()
    except KeyboardInterrupt:
        print("Exiting...")
        sleep(1)
        exit()


if __name__ == "__main__":
    main()
