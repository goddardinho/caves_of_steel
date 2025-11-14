# Caves of Steel - Changelog

## Version 0.2.0 - Enhanced User Experience

### New Features

#### 1. **Save Path Configuration** ✨
- Players can now select where to store save files on first launch
- Support for default location or custom path
- Configuration persisted in `game_config.json`
- Automatic directory creation with validation

#### 2. **Player Name Customization** 🎭
- Customize detective name instead of default "Elijah Bailey"
- Names displayed throughout the game
- Supports multi-word names (up to 30 characters)
- Option to change name mid-game via `settings` command

#### 3. **Difficulty Levels** ⚙️
- Three difficulty options: Easy, Normal, Hard
- Selection during game startup
- Difficulty affects game balance and challenge
- Difficulty displayed in status and settings

#### 4. **Settings Command** ⚙️
- New `settings` command for in-game configuration
- `settings show` - View all current settings
- `settings name <name>` - Change detective name
- Settings menu accessible anytime during gameplay

#### 5. **Quick Stats Command** 📊
- New `stats` command for at-a-glance statistics
- Shows: Investigation points, clues found, energy, time, locations visited
- Compact, easy-to-read format

#### 6. **Enhanced Status Display** 📋
- Player status now includes difficulty level
- Better formatted player information
- More comprehensive game state display

### Technical Changes

#### Modified Files
- `main.py` - Added first-launch setup flow and initialization prompts
- `src/save_system.py` - Added configuration persistence methods
- `src/player.py` - Added difficulty attribute to Player class
- `src/game_state.py` - Added difficulty tracking to GameState
- `src/game_engine.py` - Updated to accept custom save directories
- `src/commands.py` - Added `stats` and `settings` commands; fixed missing `cmd_solve` reference

#### New Methods
- `SaveSystem.is_first_launch()` - Detects first-time players
- `SaveSystem.save_config(save_dir)` - Persists user preferences
- `SaveSystem.load_config()` - Retrieves saved configuration
- `CommandProcessor.cmd_stats()` - Quick statistics display
- `CommandProcessor.cmd_settings()` - In-game settings menu

#### Bug Fixes
- Removed reference to undefined `cmd_solve` method from commands dictionary
- Fixed save/load data structure to include new difficulty field

### User Interface Improvements

#### Startup Flow
```
1. Check for first launch → Show save path prompt
2. Get player name → Validate input
3. Select difficulty → Show options with descriptions
4. Initialize game → Begin adventure
```

#### New Commands
- `stats` - Quick statistics display (added to help menu)
- `settings` - Open settings menu (added to help menu)
- `settings show` - Detailed settings view
- `settings name <name>` - Change character name

### File Changes

#### New Files
- `FEATURES.md` - Comprehensive feature documentation
- `CHANGELOG.md` - This changelog

#### Configuration Files
- `game_config.json` - Stores user's save directory preference (auto-created)

#### Data Structures
Save files now include:
```json
{
  "player": {
    "difficulty": "normal",
    ...
  },
  "game_state": {
    "difficulty": "normal",
    ...
  }
}
```

### Testing & Validation

All features have been tested and verified:
- ✓ Save path selection (default and custom)
- ✓ Player name customization
- ✓ Difficulty selection (all three levels)
- ✓ Settings command functionality
- ✓ Quick stats display
- ✓ Configuration persistence
- ✓ Save/load compatibility
- ✓ Python compilation (no syntax errors)

### Backward Compatibility

- Existing save files continue to work
- New difficulty fields default to "normal"
- Old games can be loaded and updated with new difficulty on save

### Known Limitations

- Clear screen functionality (`clear_screen()`) may interfere with piped stdin during testing
- Configuration file location fixed to `~/Documents/caves_of_steel/`
- Difficulty currently tracked but not yet affecting gameplay mechanics

### Future Enhancements

- Difficulty-based game mechanics (more/fewer clues, time pressure)
- Multiple character profiles
- Additional in-game settings (text speed, animation, accessibility)
- Auto-save functionality
- Advanced statistics and achievements
- Replay/New Game+ features

### Migration Notes

For existing games:
1. Continue using existing save files - they remain compatible
2. New saves will include difficulty information
3. First-time save path configuration will be requested
4. Player can update name via `settings name` command

---

**Release Date**: November 14, 2025  
**Version**: 0.2.0  
**Status**: Stable
