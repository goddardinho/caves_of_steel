#!/usr/bin/env python3
"""
Entry point for The Caves of Steel text adventure game
Run: python3 main.py
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game_engine import GameEngine
from src.game_state import GameState
from src.player import Player
from src.save_system import SaveSystem


def prompt_for_save_path():
    """Prompt user to select a save path on first launch.
    
    Returns:
        str: Path to save directory
    """
    print("\n" + "=" * 60)
    print("WELCOME TO THE CAVES OF STEEL")
    print("=" * 60)
    print("\nThis appears to be your first time playing.")
    print("Please select where you'd like to store game saves:\n")
    
    default_path = SaveSystem.DEFAULT_SAVE_DIR
    
    print(f"1. Default location: {default_path}")
    print("2. Custom location (enter your own path)")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            return str(default_path)
        elif choice == "2":
            custom_path = input("\nEnter the full path for saves (e.g., /Users/username/my_saves): ").strip()
            custom_path = os.path.expanduser(custom_path)  # Handle ~ expansion
            
            # Validate the path
            try:
                Path(custom_path).mkdir(parents=True, exist_ok=True)
                print(f"✓ Using save location: {custom_path}\n")
                return custom_path
            except Exception as e:
                print(f"❌ Error creating directory: {e}")
                print("Please try again.\n")
        else:
            print("❌ Invalid choice. Please enter 1 or 2.\n")


def prompt_for_player_name():
    """Prompt user to enter their detective name.
    
    Returns:
        str: Player name
    """
    while True:
        name = input("\nEnter your detective name (or press Enter for 'Elijah Bailey'): ").strip()
        if not name:
            name = "Elijah Bailey"
        if len(name) > 30:
            print("❌ Name too long (max 30 characters). Please try again.")
            continue
        return name


def prompt_for_difficulty():
    """Prompt user to select game difficulty.
    
    Returns:
        str: Difficulty level (easy, normal, hard)
    """
    print("\nSelect difficulty level:\n")
    print("1. Easy    - More clues, relaxed time limits, helpful hints")
    print("2. Normal  - Balanced gameplay (recommended)")
    print("3. Hard    - Fewer clues, strict time limits, challenging puzzles")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("✓ Difficulty set to Easy\n")
            return "easy"
        elif choice == "2":
            print("✓ Difficulty set to Normal\n")
            return "normal"
        elif choice == "3":
            print("✓ Difficulty set to Hard\n")
            return "hard"
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.\n")


def main():
    """Main entry point for the game."""
    # Check if first launch and prompt for save path
    if SaveSystem.is_first_launch():
        save_dir = prompt_for_save_path()
        SaveSystem.save_config(save_dir)
    else:
        save_dir = SaveSystem.load_config()
    
    print("\n" + "=" * 60)
    print("THE CAVES OF STEEL")
    print("A Text Adventure Game")
    print("Based on Isaac Asimov's Classic Novel")
    print("=" * 60)
    
    # Prompt for player name and difficulty
    player_name = prompt_for_player_name()
    difficulty = prompt_for_difficulty()
    
    # Initialize game
    player = Player(player_name,
                    starting_location="bedroom",
                    difficulty=difficulty)
    game_state = GameState(difficulty=difficulty)
    engine = GameEngine(player, game_state, save_dir)
    
    # Start the game
    engine.run()


if __name__ == "__main__":
    main()
