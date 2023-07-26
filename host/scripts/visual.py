def show_player_names(players: dict) -> None:
    for player in players.values():
        player.print_raw_name()


def show_player_login_infos(players: dict) -> None:
    for player in players.values():
        player.print_login()


def show_player_points(players: dict) -> None:
    for player in players.values():
        player.print_points_with_name()
