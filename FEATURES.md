# Caves of Steel - New Features

## Overview
This document describes the new features added to enhance the player experience and provide greater customization and control over gameplay.

---

## 1. Save Path Configuration (First Launch)

### Feature
On first launch of the game, players are prompted to select where they want to store their save files.

### How it Works
- **Detection**: The game checks if `game_config.json` exists
- **Options Presented**:
  1. Default location: `~/Documents/caves_of_steel/saves`
  2. Custom location: Enter your own path (supports `~` expansion)
- **Persistence**: The selected path is saved to `game_config.json` and reused for all future launches

### Configuration File
- **Location**: `~/Documents/caves_of_steel/game_config.json`
- **Format**:
  ```json
  {
    "save_dir": "/path/to/save/directory"
  }
  ```

### Technical Implementation
- `SaveSystem.is_first_launch()` - Checks if config exists
- `SaveSystem.save_config(save_dir)` - Persists the selected path
- `SaveSystem.load_config()` - Retrieves saved path on subsequent launches

---

## 2. Player Name Customization

### Feature
Players can enter a custom name for their detective character instead of being stuck with "Detective".

### How it Works
- **Prompt**: After selecting save path, players are asked to enter their detective name
- **Validation**: Names are limited to 30 characters
**Default**: Pressing Enter without typing uses "Elijah Baley"
- **Display**: The custom name appears in:
  - Character status displays
  - Save files
Enter your detective name (or press Enter for 'Elijah Baley'): Sherlock Holmes
  - Detective status formatting

### Example
```
Enter your detective name (or press Enter for 'Detective'): Sherlock Holmes
✓ Character created: Sherlock Holmes
```

---

## 3. Difficulty Levels

### Feature
Players can choose from three difficulty levels that affect game balance and challenge.

### Difficulty Options

| Level | Description | Features |
|-------|-------------|----------|
| **Easy** | More clues, relaxed time limits, helpful hints | Best for exploring and enjoying the story |
| **Normal** | Balanced gameplay (recommended) | Standard experience with good pacing |
| **Hard** | Fewer clues, strict time limits, challenging puzzles | For experienced players seeking a challenge |

### How it Works
- **Selection**: During startup, players choose difficulty from the menu
- **Storage**: Difficulty is saved in the game save file
- **Impact**: Can be used to adjust game mechanics (AI hints, time pressure, etc.)

### Technical Implementation
- `Player.difficulty` - Stores player's chosen difficulty
- `GameState.difficulty` - Tracks game difficulty settings
- Saved in both player and game_state data

---

## 4. Settings Command

### Feature
Access and modify game settings during gameplay with the `settings` command.

### Available Options

#### `settings`
Opens the settings menu and shows current player name and difficulty.

#### `settings show`
Displays comprehensive current game settings including:
- Detective name
- Difficulty level
- Current location
- Investigation points
- Energy level
- Day and time of day

#### `settings name <new_name>`
Changes the detective's name mid-game.

**Example**:
```
🎮 > settings name Columbo
✓ Detective name changed from 'Sherlock Holmes' to 'Columbo'
```

---

## 5. Quick Stats Command

### Feature
Display game statistics at a glance with the `stats` command.

### Information Displayed
- Detective name
- Difficulty level
- Investigation points
- Clues found count
- Energy level
- Current day and time
- Locations visited count

### Example Output
```
==================================================
QUICK STATS
==================================================
Detective: Elijah Baley
Difficulty: Hard
Investigation Points: 45
Clues Found: 3
Energy Level: 85%
Day: 2 - Evening
Locations Visited: 5
==================================================
```

---

## 6. Enhanced Status Display

### Feature
The player's status now includes difficulty level information.

### Updated Display
```
┌─ DETECTIVE STATUS ─────────────────────┐
│ Name: Sherlock Holmes
│ Difficulty: Hard
│ Location: bedroom
│ Energy: 85%
│ Investigation Points: 45
│ Clues Found: 3
└────────────────────────────────────────┘
```

---

## User Experience Flow

### First Time Playing
1. Game detects first launch
2. User selects save location (default or custom)
3. User enters detective name
4. User selects difficulty level
5. Game begins

### Subsequent Launches
1. Game loads saved configuration automatically
2. User enters name and difficulty for new game
3. Game begins (save location remembered)

### During Gameplay
- Use `stats` for quick stats overview
- Use `status` for detailed player and game information
- Use `settings` to change name mid-game
- Use `help` to see all available commands

---

## File Structure

### Configuration Files
```
~/Documents/caves_of_steel/
├── game_config.json          # Stores save directory preference
└── saves/                    # Directory containing save files
    ├── save_20251114_153045.json
    ├── save_20251114_154312.json
    └── ...
```

### Modified/New Code
- `main.py` - First-launch setup flow
- `src/save_system.py` - Configuration persistence methods
- `src/player.py` - Difficulty attribute
- `src/game_state.py` - Difficulty attribute
- `src/game_engine.py` - Support for custom save directories
- `src/commands.py` - New settings and stats commands

---

## Technical Details

### SaveSystem Enhancements
```python
SaveSystem.is_first_launch()      # Check if config exists
SaveSystem.save_config(path)      # Persist configuration
SaveSystem.load_config()          # Load saved configuration
SaveSystem(custom_save_dir)       # Initialize with custom path
```

### Player/GameState Updates
```python
Player(name, location, difficulty="normal")
GameState(difficulty="normal")
```

### New Commands
- `stats` - Quick statistics display
- `settings` - Settings menu
- `settings show` - Show all settings
- `settings name <name>` - Change character name

---

## Future Enhancements

Potential improvements for future versions:
- Save multiple character profiles
- Difficulty-based rewards and achievements
- Configurable game settings (animation speed, text speed, etc.)
- Accessibility options (color schemes, text size, etc.)
- Language selection
- Auto-save functionality at key points
- Performance settings

---

## Testing Notes

To test these features:

1. **First Launch**: Delete `game_config.json` to trigger first-launch flow
2. **Custom Names**: Test names with spaces, special characters, unicode
3. **Difficulty Selection**: Verify all three difficulty levels work correctly
4. **Settings Menu**: Test `settings`, `settings show`, `settings name` commands
5. **Save/Load**: Verify difficulty and name persist through save/load cycles

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Game doesn't prompt for name/difficulty | Check that `game_config.json` was created correctly |
| Save path shows as "1" or partial name | Ensure heredoc or proper stdin redirection when testing |
| Settings not saving | Verify directory permissions for `~/Documents/caves_of_steel/` |
| Difficulty not persisting | Check that save file includes `difficulty` field |

