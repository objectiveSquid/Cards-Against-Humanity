from scripts.checks import can_see_played_cards, can_vote_winner, can_play_cards, auth
from scripts.randomness import choose_random_question, choose_random_card
from scripts.extract import get_points_from_players
from scripts.disk import read_questions, read_cards
from flask import Response, request, jsonify, Flask
from scripts.visual import show_player_login_infos
from scripts.get_settings import get_settings
from scripts.generate import generate_players
from threading import Thread
from colorama import Fore
from time import sleep

HOST = "0.0.0.0"
PORT = "80"

app = Flask(__name__)


@app.route("/play-cards", methods=["POST"])
def play_cards() -> Response:
    global vote_in_progress, required_cards, game_ending, card_pool, players, cards

    data: dict[str, str | list[str]] = request.json
    username = data.get("username")
    key = data.get("key")
    cards = data.get("cards")

    authenticated = can_play_cards(
        key, username, required_cards, card_pool, cards, players
    )

    if not authenticated[0]:
        return Response(authenticated[1], 403)

    card_pool[username] = cards

    try:
        return jsonify([choose_random_card(cards) for _ in range(required_cards)])
    except IndexError:
        game_ending = True
        return Response("game is now ending", 202)


@app.route("/played-cards", methods=["GET"])
def played_cards() -> Response:
    global vote_in_progress, card_pool, players

    data: dict[str, str] = request.json
    username = data.get("username")
    key = data.get("key")

    authenticated = can_see_played_cards(key, username, vote_in_progress, players)
    if not authenticated[0]:
        return Response(authenticated[1], 403)

    return jsonify(card_pool)


@app.route("/played-players", methods=["GET"])
def played_players() -> Response:
    global card_pool, players

    data: dict[str, str] = request.json
    username = data.get("username")
    key = data.get("key")

    authenticated = auth(key, username, players)
    if not authenticated[0]:
        return Response(authenticated[1], 403)

    return jsonify(list(card_pool.keys()))


@app.route("/held-cards", methods=["GET"])
def held_cards() -> Response:
    global players

    data: dict[str, str] = request.json
    username = data.get("username")
    key = data.get("key")

    authenticated = auth(key, username, players)
    if not authenticated[0]:
        return Response(authenticated[1], 403)

    player = players[username]
    return jsonify(player.cards)


@app.route("/vote-winner", methods=["POST"])
def vote_winner() -> Response:
    global vote_in_progress, card_pool, players

    data: dict[str, str] = request.json
    username = data.get("username")
    key = data.get("key")
    selected_winner = data.get("winner")

    authenticated = can_vote_winner(
        key, username, selected_winner, vote_in_progress, players
    )
    if not authenticated[0]:
        return Response(authenticated[1], 403)

    winner_player = players.get(selected_winner)
    winner_player.increase_round_score()
    player = players.get(username)
    player.set_has_voted()

    return Response("vote counted", 200)


@app.route("/active-question", methods=["GET"])
def send_active_question() -> Response:
    global active_question

    return Response(active_question, 200)


@app.route("/player-names", methods=["GET"])
def send_player_amount() -> Response:
    global players

    return jsonify(list(players.keys()))


@app.route("/winners", methods=["GET"])
def send_winners() -> Response:
    global game_ending, players

    if not game_ended:
        return Response("game has not yet ended, please wait", 503)

    return jsonify(get_points_from_players(players))


@app.route("/is-voting", methods=["GET"])
def is_voting() -> Response:
    global vote_in_progress

    if vote_in_progress:
        return Response("vote is in progress, please wait", 200)
    return Response("players are submitting their cards, please wait", 503)


@app.route("/game-ending", methods=["GET"])
def is_game_ending() -> Response:
    global game_ending

    if game_ending:
        return Response("ran out of cards to distribute, game is ending", 200)
    return Response("game is not ending", 503)


@app.route("/check-credentials", methods=["GET"])
def check_credentials() -> Response:
    global players

    data: dict = request.json
    username = data.get("username")
    key = data.get("key")

    authenticated = auth(key, username, players)
    return Response(authenticated[1], 200 if authenticated[0] else 403)


def wait_for_submits() -> None:
    global active_question, required_cards, game_ending, game_ended, card_pool, players

    if game_ending:
        game_ended = True
        while True:
            sleep(0.5)  # do nothing, the game has ended

    required_cards = active_question.count("{}")

    while len(card_pool) != len(players):
        sleep(0.5)

    wait_for_votes()


def wait_for_votes() -> None:
    global vote_in_progress, active_question, winner_points, round_winner, non_voters, questions, card_pool, players

    vote_in_progress = True
    while vote_in_progress:
        for player in players.values():
            if player.name not in non_voters and player.has_voted:
                non_voters.append(player.name)
                continue
            vote_in_progress = False
            break

    round_winner = ""
    card_pool = {}
    non_voters = []
    winner_points = ([], -1)

    for player in players.values():
        if winner_points[1] < player.round_score:
            winner_points = [player.name], player.round_score
        elif winner_points[1] == player.round_score:
            winner_points[0].append(
                player.name
            )  # this is so multiple players can have the same top score, and still share first place
        player.remove_has_voted()
        player.clear_round_score()

    active_question = choose_random_question(questions)
    wait_for_submits()


def main() -> None:
    """cards: all cards read from data/cards.txt
    round_winner: winner of current round, if empty - the winner has not yet been chosen
    card_pool: cards that players have played in this round
    required_cards: the amount of cards to be played by each player
    players: dict of players looking like this {"player_name": Player}
    active_question: the active question card
    non_voters: player names who have yet to vote for a winner
    vote_in_progress: if a vote is in progress (no winner chosen or not all players have submitted cards)
    game_ending: ran out of cards to distribute
    game_ended: ran out of cards to distribute and all players have voted
    """
    global vote_in_progress, active_question, required_cards, round_winner, game_ending, game_ended, non_voters, questions, card_pool, players, cards
    SETTINGS = get_settings()
    PLAYER_NAMES = SETTINGS["player_names"]
    CARDS_PER_PLAYER = SETTINGS["cards_per_player"]
    required_cards = 0
    non_voters = []
    card_pool = {}
    round_winner = ""
    vote_in_progress = False
    game_ending = False
    game_ended = False
    questions = read_questions()
    active_question = choose_random_question(questions)
    cards = read_cards()
    players = generate_players(PLAYER_NAMES, cards, CARDS_PER_PLAYER)
    show_player_login_infos(players)

    print(f"{Fore.YELLOW}Setup done, starting Flask webserver.{Fore.RESET}")

    Thread(target=wait_for_submits, name="wait for submits/votes thread").start()
    app.run(HOST, PORT)


if __name__ == "__main__":
    main()
