from typing import Iterable
from os import name

if name == "nt":
    from msvcrt import getch
else:
    import sys, tty, termios

    def getch() -> (
        bytes
    ):  # taken from https://stackoverflow.com/questions/510357/how-to-read-a-single-character-from-the-user
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return character


def string_format(string_to_format: str, *args: Iterable[str]) -> str:
    for arg in args:
        try:
            string_to_format = string_to_format.format(arg)
        except IndexError:
            break
    return string_to_format
