from scripts.player import Player


def get_points_from_players(players: dict[str, Player]) -> list[tuple[str, int]]:
    output = []

    for player in players.values():
        output.append((player.name, player.points))

    output.sort(key=lambda output: output[1], reverse=True)

    return output
