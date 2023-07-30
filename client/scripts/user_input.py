from scripts.warns import NAME_NOT_FOUND, NUM_TOO_SMALL, NUM_TOO_LARGE, INVALID_INT
from scripts.alternatives import getch
from scripts.msgs import ASK_WINNER
from typing import Iterable


def getch_int(
    min: int = 0,
    max: int | None = None,
    other_allowed: Iterable[str] | None = None,
) -> int | str:
    if other_allowed == None:
        other_allowed = []
    while True:
        try:
            getch_output = getch()
            decoded_getch_output = getch_output.decode()
            number = int(getch_output)
        except ValueError:
            if getch_output == b"\x03":  # code for ctrl+c:
                raise KeyboardInterrupt
            if decoded_getch_output not in other_allowed:
                print(INVALID_INT)
                continue
            return decoded_getch_output
        if number < min:
            print(NUM_TOO_SMALL)
            continue
        elif number > max and max != None:
            print(NUM_TOO_LARGE)
            continue
        return number


def get_winner_name(player_names: Iterable[str]) -> str:
    player_names = [player_name.lower() for player_name in player_names]
    winner_name = input(ASK_WINNER).strip().lower()
    if winner_name not in player_names:
        print(NAME_NOT_FOUND)
        return get_winner_name(player_names)
    return winner_name
