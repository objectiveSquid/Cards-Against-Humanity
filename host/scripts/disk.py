def read_cards() -> list[str]:
    with open("data/cards.txt") as cards_file:
        return cards_file.read().splitlines()


def read_questions() -> list[str]:
    with open("data/questions.txt") as questions_file:
        return questions_file.read().splitlines()
