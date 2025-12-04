# Caves of Steel - Changelog

## Version 0.4.0 - Complete Plot Implementation & NPC Personalization

### Major Features

#### 1. **Complete "Caves of Steel" Plot Integration** 📖
- Full plot implementation based on Isaac Asimov's classic novel
- Political factions system with three competing ideologies:
  - **Spacer Expansionists**: Promote human-robot cooperation and galactic colonization
  - **Medievalists**: Anti-robot faction seeking to preserve human Earth culture
  - **Earth Officials**: Government maintaining status quo
- Murder mystery: Dr. Roj Nemennuh Sarton death investigation
- Mistaken identity plot: Julius Enderby (secretly Medievalist) murders Sarton intending to kill R. Daneel
- Multiple resolution paths leading to different endings

#### 2. **All 10 Main Book Characters as NPCs** 👥
Complete implementation of all principal characters:
- **Elijah "Lije" Baley** - Series protagonist detective
- **R. Daneel Olivaw** - Humanoid robot partner
- **Julius Enderby** - Police Commissioner (actual killer)
- **Jessie Bailey** - Lije's wife with growing concerns
- **Ben Bailey** - Young son fascinated by robots
- **Vince Barrett** - Disgruntled junior officer losing position to robots
- **R. Sammy** - Service robot (weapon accomplice, not guilty)
- **Han Fastolfe** - Spacer diplomat advancing robot-human agenda
- **Dr. Anthony Gerrigel** - Robotics scientist
- **Francis Clousarr** - Medievalist militant anti-robot activist

Each NPC includes:
- Unique dialogue trees with character-specific responses
- Detailed physical examination descriptions
- Relationship tracking with trust/suspicion values
- Investigation clues and plot-relevant information

#### 3. **Investigation System with Evidence Tracking** 🔍
- Multi-category investigation command: `investigate <category>`
- Five evidence types tracked:
  1. **Eyeglasses Evidence** - Broken glasses at crime scene (key forensic evidence)
  2. **Enderby Information** - Clues about Commissioner's guilt
  3. **R. Sammy Involvement** - Weapon transport conspiracy
  4. **Spacer Conspiracy** - Political faction context
  5. **Suspect Information** - Character-specific investigation data
- Evidence counter displays progress (e.g., "Evidence Found: 3/5")
- Eyeglasses collected and examined with forensic analysis
- Investigation points system for detective progression

#### 4. **Dynamic Mystery Tracking** 📊
- Seven suspects with individual alibis
- Suspects Questioned counter (0/7)
- Alibis Verified counter (0/7)
- Evidence Found counter (0/5)
- 90-minute deadline for Spacer departure (time pressure element)
- Real-time investigation status in mystery command

#### 5. **Multiple Endings System** 🎭
Two distinct resolution paths:

**Perfect Justice Ending** ⚖️
- Triggered when sufficient evidence (4-5 clues) collected
- Julius Enderby convicted for Sarton's murder
- Spacer expansion agenda halted
- Traditional justice system upheld
- Earth maintains anti-robot status quo

**Spacer Resolution Ending** 🚀
- Triggered with partial evidence (2-3 clues)
- Spacers negotiate Enderby's freedom for colonization work
- Enderby continues as Commissioner (corruption tolerated)
- Human-robot cooperation begins on Earth
- Spacers gain strategic foothold for human colonization
- Justice compromised for political progress

#### 6. **NPC First-Name Alias System** 🎤
- Players can now interact with NPCs using first names (case-insensitive)
- 30+ aliases configured for natural interaction:
  - `daneel` → R. Daneel Olivaw
  - `julius` → Julius Enderby
  - `jessie` → Jessie Bailey
  - `ben` → Ben Bailey
  - And 26+ others
- Works across all NPC commands: `talk`, `examine`, `ask`, `play`, `comfort`
- Enhanced immersion and personal connection with characters

### Technical Features

#### 1. **Faction Class** (New Data Structure)
- `name`: Faction identifier
- `ideology`: Core beliefs
- `goal`: Political objective
- `methods`: How faction operates
- Full faction details tracked for detective use

#### 2. **Enhanced Mystery Plot** (src/mystery_plot.py)
- Seven suspects vs. previous single culprit tracking
- `key_evidence` tracking for all 5 evidence types
- `record_evidence()` method for investigation flow
- Actual killer identified: Julius Enderby
- Accomplice tracking: R. Sammy (involved but not guilty of murder)
- Mistaken identity context preserved in investigation

#### 3. **Demo Mode Non-Blocking Execution**
- `demo_mode` flag prevents input() blocking in non-interactive environments
- Branching dialogue defaults to choice 1 when demo_mode=True
- Enables automated testing and demo execution

#### 4. **Five New Locations** 🗺️
- `robot_division` - Where R. Sammy works
  - `spacetown` - Han Fastolfe's headquarters (renamed from `spacer_embassy`)
- `robotics_lab` - Dr. Gerrigel's research facility
- `detention_block` - Francis Clousarr's holding area
- Each location contains relevant NPCs and clues

### Commands & Gameplay

#### New Commands
- `investigate <category>` - Multi-category investigation system
  - `investigate eyeglasses` - Forensic analysis of broken glasses
  - `investigate enderby` - Commissioner guilt clues
  - `investigate sammy` - Robot accomplice information
  - `investigate spacer_conspiracy` - Political faction context
- `accuse <npc_name>` - Accusation system triggering appropriate ending

#### Enhanced Commands
- `talk <first_name or full_name>` - Works with both formats
- `examine <first_name or full_name>` - NPC examination with name resolution
- `ask <first_name> <topic>` - Family-focused dialogue with aliases
- `play <first_name>` - Play with Ben using any alias
- `comfort <first_name>` - Comfort Jessie using any alias
- `mystery` - Enhanced to show all investigation counters

### User Interface Improvements

#### Investigation Status Display
```
╔═════════════════════════════════════════╗
║          MURDER INVESTIGATION           ║
├─────────────────────────────────────────┤
║ Victim: Dr. Roj Nemennuh Sarton
║ Cause: Blaster wound
║ Time: between 14:45 and 16:00
║ Suspects Questioned: 0/7
║ Alibis Verified: 0/7
║ Evidence Found: 3/5
║ Time Until Spacers Leave: 90 min
╚═════════════════════════════════════════╝
```

#### Ending Narratives
- Detailed, emotionally resonant conclusions
- Character-driven resolution explaining:
  - Killer's identity and motive
  - Political implications
  - Character fate (Enderby's continued promotion)
  - Larger thematic meaning (justice vs. progress)

### File Changes

#### Modified Files
- `src/mystery_plot.py` - Added Faction class, seven suspects, evidence tracking
- `src/commands.py` - Added investigate command, NPC_NAME_MAP (30+ aliases), name resolution
- `src/game_engine.py` - Added demo_mode flag and passing
- `src/dialogue_system.py` - Expanded NPC dialogue with plot context
- `src/locations.py` - Added eyeglass_evidence, five new locations
- `src/endings.py` - Replaced with two new endings (perfect_justice, spacer_resolution)
- `main.py` - Updated demo commands to showcase investigation flow

#### Data Structures Updated
```python
# Faction class added
class Faction:
    name: str
    ideology: str
    goal: str
    methods: str

# MysteryPlot updated with
actual_killer = "Julius Enderby"
key_evidence = {}  # Tracks 5 evidence types
suspects = [7 characters]  # Extended from 1-2 to full list
```

### Testing & Validation

All features tested and verified:
- ✓ Demo mode runs to completion without hanging
- ✓ All 11 NPCs spawn in correct locations
- ✓ Investigation system identifies correct killer
- ✓ Both endings trigger appropriately based on evidence
- ✓ Name alias system works across all NPC commands
- ✓ Eyeglasses evidence collects and displays correctly
- ✓ Faction system tracks political dynamics
- ✓ All code compiles without syntax errors
- ✓ Save/load compatible with previous versions

### Bug Fixes

- Fixed demo mode hanging on branching dialogue (input() blocking)
- Removed "(mistaken identity)" from murder display while maintaining tracker
- Ensured eyeglasses evidence properly located and examinable
- Corrected R. Sammy involvement (accomplice, not killer)

### Gameplay Improvements

- **Immersive NPC Interaction**: First-name aliases create personal connections
- **Multiple Solutions**: Evidence gathering affects ending (not just accuser)
- **Political Complexity**: Faction system adds moral ambiguity to justice
- **Time Pressure**: 90-minute Spacer deadline increases urgency
- **Character Development**: All NPCs have meaningful roles in plot

### Known Limitations

- Difficulty levels still tracked but not affecting gameplay
- Spacer conspiracy details limited to investigation hints
- Limited branching dialogue (choices default to 1 in demo mode)
- No alternate suspect accusations (Enderby is always correct)

### Future Enhancements

- Difficulty-based investigation complexity (fewer/more clues)
- Alternative suspect accusations with consequences
- Extended dialogue tree branching
- Character backstory subplots
- Achievement system (justice vs. pragmatism tracking)
- New Game+ with variations

### Migration Notes

For existing saves from v0.2.0/v0.3.0:
1. Old saves remain compatible but won't have investigation data
2. New investigation features only available in new games
3. NPC aliases work for all new interactions
4. Multiple endings automatically determined by evidence collected

---

**Release Date**: November 17, 2025  
**Version**: 0.4.0  
**Status**: Stable

## Version 0.2.0 - Enhanced User Experience

### New Features

#### 1. **Save Path Configuration** ✨
- Players can now select where to store save files on first launch
- Support for default location or custom path
- Configuration persisted in `game_config.json`
- Automatic directory creation with validation

#### 2. **Player Name Customization** 🎭
- Customize detective name instead of default "Elijah Baley"
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

## Version 0.7.0 - December 4, 2025

### Major Changes
- All references to 'Elijah Bailey' corrected to 'Elijah Baley' throughout code and documentation.
- Enhanced `settings` command: now supports changing detective name, difficulty, text speed, and accessibility mode, with improved menu/help text.
- Expanded `help` command output: added detailed settings and navigation instructions for better usability.
- Typing `exit` no longer quits the game; only `quit` will exit. `exit` now shows an unknown command message.
- Removed non-canonical NPC 'Commander Lije Bailey' from all code and documentation.
- Renamed 'Spacer Embassy' to 'Spacetown' everywhere (location key, display name, alibi text, changelog).
- Migrated major features section from changelog to `TODO.md` for ongoing planning and visibility.
- Confirmed all modified files compile and demo runs successfully.

### Refactors & Documentation
- Improved codebase consistency and accuracy with book canon.
- Updated changelog and TODO.md to reflect current feature set and refactors.

---
