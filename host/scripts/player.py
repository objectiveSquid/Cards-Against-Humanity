from scripts.randomness import generate_key
from sys import stdout


class Hand:
    def __init__(self, cards: list[str]) -> None:
        self.cards = cards

    def give_new_card(self, card: str) -> None:
        self.cards.append(card)

    def print_cards(self) -> None:
        print(*self.cards, sep="\n")


class Player(Hand):
    def __init__(
        self, player_name: str, key_length: int = 12, cards: list[str] = None
    ) -> None:
        if cards == None:
            cards = []
        super().__init__(cards)
        self.name = player_name.title()
        self.points = 0
        self.round_score = 0
        self.key = generate_key(key_length)
        self.has_voted = False

    def remove_has_voted(self) -> None:
        self.has_voted = False

    def set_has_voted(self) -> None:
        self.has_voted = True

    def clear_round_score(self) -> None:
        self.round_score = 0

    def increase_round_score(self) -> None:
        self.round_score += 1

    def give_point(self) -> None:
        self.points += 1

    def print_login(self) -> None:
        print(f"{self.name}: {self.key}")

    def print_name(self) -> None:
        print(f"Name: {self.name}")

    def print_raw_name(self) -> None:
        print(self.name)

    def print_points_with_name(self) -> None:
        print(f"{self.name}: {self.points}")

    def print_points(self) -> None:
        print(f"Points: {self.points}")

    def print_info(self) -> None:
        self.print_name()
        self.print_points()

    def print_info_and_cards(self) -> None:
        self.print_info()
        stdout.write("Cards: ")
        self.print_cards()
