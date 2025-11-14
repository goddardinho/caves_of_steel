# The Caves of Steel - Text Adventure Game

A text-based interactive adventure game inspired by Isaac Asimov's classic science fiction novel "The Caves of Steel"

## Story

You are a detective living in New York City in the year 4956 AD. Humanity has retreated underground into massive cave cities to escape the surface. A murder has been committed, and you must solve it. What makes this case unusual is that you've been assigned an unusual partner: R. Daneel Olivaw, a humanoid robot from the Outer Regions.

The investigation will take you through the depths of the Caves of Steel—from your modest quarters to crowded plazas, administrative sectors, and crime scenes. You'll meet diverse characters, uncover clues, and work to solve a mystery that may have larger implications for human-robot relations.

## Features

- **Rich Text-Based World**: Explore the underground cave city of New York
- **Complete Murder Mystery**: Investigate a detailed murder plot with suspects and motives
- **Detective Gameplay**: Gather clues, interrogate suspects, solve puzzles, and accuse the killer
- **Dialogue Choice Trees**: Interactive conversations with NPCs that affect relationships
- **NPC Relationship System**: Track your relationships with characters (trust/hostility)
- **Puzzle-Solving Elements**: Logic puzzles, access codes, and pattern recognition
- **Time-Based Events**: Events trigger at specific times during the investigation
- **Multiple Endings**: 5 different endings based on your choices and investigation quality
- **Inventory System**: Pick up and manage evidence items
- **Save/Load System**: Save your progress at any time
- **Game State Tracking**: Track investigation points, clues, and progress

## Getting Started

### Requirements

- Python 3.7+
- No external dependencies required (uses only Python standard library)

### Installation

```bash
cd caves_of_steel
python3 main.py
```

## How to Play

### Available Commands

**Movement:**
- `go <direction>` - Move to another location (e.g., `go plaza`, `go administrative`)

**Interaction:**
- `look` - Look around and see your current status
- `examine <object>` - Examine an item or person closely
- `talk <to person>` - Speak with an NPC (e.g., `talk to commissioner`)
- `take <item>` - Pick up an item
- `take all` - Pick up all items in a location
- `drop <item>` - Drop an item from your inventory
- `drop all` - Drop all items from your inventory

**Investigation:**
- `mystery` - Show murder mystery details and suspects
- `accuse <person>` - Accuse someone of the murder (requires sufficient evidence)
- `relationships` - Show your relationship status with all NPCs
- `puzzle <id>` - Attempt to solve a puzzle or get a hint

**Information:**
- `inventory` or `i` - Show what you're carrying
- `status` - Show your detective status and found clues
- `help` - Show all available commands

**Save/Load:**
- `save` or `s` - Save your game progress
- `load` or `l` - Load a previous save

**Game:**
- `quit` - Exit the game

### Tips for Playing

1. **Explore thoroughly** - Visit all locations and talk to all NPCs
2. **Examine everything** - Look at objects and people carefully for clues
3. **Collect evidence** - Pick up items that might be relevant to the case
4. **Track clues** - Use the `status` command to see what you've learned
5. **Build relationships** - Your interactions with characters matter
6. **Pay attention to details** - Descriptions contain important information

## Game Locations

- **Your Quarters** - Your small apartment where you start
- **Residential Corridor** - The hallway connecting residential areas
- **Central Plaza** - Heart of the underground city
- **Police Headquarters** - Where you get your case assignment
- **Commissioner's Office** - Meet your robot partner here
- **Administrative Section** - Government offices and bureaucracy
- **Records Office** - Access citizen information
- **Food Dispensary** - Where citizens get their nutrition
- **Crime Scene** - Investigate the murder location

## Story Context

Based on Isaac Asimov's 1954 novel "The Caves of Steel," this game captures the detective noir atmosphere of the book while allowing players to explore the themes of:

- Human vs. robot relationships
- Justice in an underground society
- The investigation process and deductive reasoning
- Societal structure and prejudice

## Development

This game is built in modular Python, making it easy to extend with:

- Additional locations and NPC dialogue
- New puzzles and mystery elements
- Extended investigation mechanics
- Complex relationship trees
- Custom events and endings

### Core Systems

- **Mystery Plot System** - Complete investigation with suspects and motives
- **Relationship Manager** - Track trust/hostility with all NPCs
- **Puzzle Manager** - Interactive puzzles with hints and solutions
- **Dialogue System** - Choice-based conversations with NPCs
- **Event Manager** - Time-triggered events throughout the game
- **Endings System** - 5 different endings based on player actions
- **Save System** - Persistent save files with full game state

### Development Tools

This project uses the following tools for formatting and linting:

- `black` — opinionated code formatter (used to format source files)
- `ruff` — fast linter and fixer for Python (used to check for issues and apply small fixes)

Recommended setup (macOS / Linux):

```bash
# Install tools (user install)
python3 -m pip install --user black ruff

# Format code with Black
python3 -m black src main.py

# Run Ruff checks
python3 -m ruff check src

# Optionally, apply automatic Ruff fixes
python3 -m ruff check src --fix
```

I recommend keeping `black` and `ruff` as the authoritative tools for style. I removed `flake8` from the repository tooling to avoid overlapping rules; if you prefer `flake8`, we can reintroduce it with a configured profile.

## Future Enhancements

Potential features to add:

- Additional locations and environments
- More NPC characters with extended dialogue trees
- Advanced puzzle combinations
- Reputation system affecting case access
- Branching storylines based on relationship choices
- Multiple investigation paths
- AI-driven suspect behavior
- Procedurally generated evidence

## Author

Created as a text adventure game project inspired by Isaac Asimov's "The Caves of Steel"

## License

This is a fan-created game based on Asimov's work. Enjoy exploring the Caves of Steel!
