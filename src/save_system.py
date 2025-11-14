"""
Save System - Handle game saving and loading
"""

import json
import os
from pathlib import Path
from datetime import datetime


class SaveSystem:
    """Manages saving and loading game progress."""
    
    SAVE_DIR = Path.home() / "Documents" / "personal-text-game" / "saves"
    
    def __init__(self):
        """Initialize save system."""
        self.SAVE_DIR.mkdir(parents=True, exist_ok=True)
    
    def save_game(self, player, game_state, filename=None):
        """Save the current game state.
        
        Args:
            player: Player object
            game_state: GameState object
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            str: Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"save_{timestamp}.json"
        
        save_path = self.SAVE_DIR / filename
        
        save_data = {
            "timestamp": datetime.now().isoformat(),
            "player": {
                "name": player.name,
                "current_location": player.current_location,
                "inventory": player.inventory,
                "energy": player.energy,
                "investigation_points": player.investigation_points,
                "met_characters": list(player.met_characters),
                "clues_found": player.clues_found,
            },
            "game_state": {
                "time_period": game_state.time_period,
                "day": game_state.day,
                "case_solved": game_state.case_solved,
                "partner_assigned": game_state.partner_assigned,
                "partner_name": game_state.partner_name,
                "events_triggered": list(game_state.events_triggered),
                "visited_locations": list(game_state.visited_locations),
                "npc_states": game_state.npc_states,
            }
        }
        
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return str(save_path)
    
    def load_game(self, filename):
        """Load a saved game.
        
        Args:
            filename: Filename or path to load
            
        Returns:
            tuple: (player_data, game_state_data) or (None, None) if failed
        """
        save_path = self.SAVE_DIR / filename if not filename.startswith('/') else Path(filename)
        
        if not save_path.exists():
            return None, None
        
        try:
            with open(save_path, 'r') as f:
                save_data = json.load(f)
            return save_data.get("player"), save_data.get("game_state")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading save file: {e}")
            return None, None
    
    def list_saves(self):
        """List all available save files.
        
        Returns:
            list: List of (filename, timestamp) tuples
        """
        saves = []
        for save_file in sorted(self.SAVE_DIR.glob("save_*.json"), reverse=True):
            try:
                with open(save_file, 'r') as f:
                    data = json.load(f)
                    timestamp = data.get("timestamp", "Unknown")
                    saves.append((save_file.name, timestamp))
            except json.JSONDecodeError:
                continue
        return saves
    
    def delete_save(self, filename):
        """Delete a save file.
        
        Args:
            filename: Filename to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        save_path = self.SAVE_DIR / filename
        try:
            if save_path.exists():
                save_path.unlink()
                return True
            return False
        except OSError:
            return False
