from random import choices, randint


def generate_key(
    key_length: int,
    charset: str = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789",  # intentionally missing letters like I and 0/O to avoid mixing up letters
) -> str:
    no_split = False
    key_split = 1
    key = ""

    if (key_length % 4) == 0:
        key_split = 4
    elif (key_length % 3) == 0:
        key_split = 3
    elif (key_length % 5) == 0:
        key_split = 5
    else:
        no_split = True

    for _ in range(round(key_length / key_split)):
        key += "".join(choices(charset, k=key_split))
        if not no_split:
            key += "-"

    return key.removesuffix("-")


def choose_random_question(questions: list[str]) -> str:
    return questions.pop(randint(0, len(questions) - 1))


def choose_random_card(cards: list[str]) -> str:
    return cards.pop(randint(1, len(cards) - 1))
