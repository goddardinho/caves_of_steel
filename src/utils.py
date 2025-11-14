"""
Utility functions for the game
"""

import os
import sys


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_separator(char="─", width=60):
    """Print a separator line.

    Args:
        char: Character to use for the line
        width: Width of the line
    """
    print(f"\n{char * width}\n")


def print_box(text, width=60):
    """Print text in a box.

    Args:
        text: Text to display
        width: Width of the box
    """
    lines = text.split("\n")
    print(f"┌{'─' * (width - 2)}┐")
    for line in lines:
        print(f"│ {line:<{width - 4}} │")
    print(f"└{'─' * (width - 2)}┘")


def slow_print(text, delay=0.05):
    """Print text slowly for dramatic effect.

    Args:
        text: Text to print
        delay: Delay between characters in seconds
    """
    import time

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
