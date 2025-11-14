#!/usr/bin/env python3
"""
Entry point for The Caves of Steel text adventure game
Run: python3 main.py
"""

import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game_engine import GameEngine
from src.game_state import GameState
from src.player import Player


def main():
    """Main entry point for the game."""
    print("\n" + "=" * 60)
    print("THE CAVES OF STEEL")
    print("A Text Adventure Game")
    print("Based on Isaac Asimov's Classic Novel")
    print("=" * 60 + "\n")
    
    # Initialize game
    player = Player("Detective", starting_location="bedroom")
    game_state = GameState()
    engine = GameEngine(player, game_state)
    
    # Start the game
    engine.run()


if __name__ == "__main__":
    main()
