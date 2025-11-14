"""
Command Processor - Handles player commands
"""

from src.locations import LOCATIONS
from src.utils import print_separator


class CommandProcessor:
    """Processes and executes player commands."""
    
    def __init__(self, player, game_state):
        """Initialize command processor.
        
        Args:
            player: Player object
            game_state: GameState object
        """
        self.player = player
        self.game_state = game_state
        self.commands = {
            "look": self.cmd_look,
            "go": self.cmd_go,
            "move": self.cmd_go,
            "examine": self.cmd_examine,
            "inspect": self.cmd_examine,
            "talk": self.cmd_talk,
            "speak": self.cmd_talk,
            "inventory": self.cmd_inventory,
            "inv": self.cmd_inventory,
            "i": self.cmd_inventory,
            "take": self.cmd_take,
            "get": self.cmd_take,
            "drop": self.cmd_drop,
            "status": self.cmd_status,
            "help": self.cmd_help,
            "accuse": self.cmd_accuse,
            "relationships": self.cmd_relationships,
            "mystery": self.cmd_mystery,
            "puzzle": self.cmd_puzzle,
        }
    
    def process(self, command_string):
        """Process a player command.
        
        Args:
            command_string: The command string from the player
        """
        parts = command_string.split(maxsplit=1)
        if not parts:
            return
        
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command in self.commands:
            self.commands[command](args)
        else:
            print(f"\n❌ Unknown command: '{command}'. Type 'help' for available commands.\n")
    
    def cmd_look(self, args):
        """Look command - examine current surroundings."""
        print(f"\n{self.player.get_status()}\n")
    
    def cmd_go(self, args):
        """Go/move command - move to another location.
        
        Args:
            args: Direction or location name
        """
        if not args:
            print("\n❌ Go where? Please specify a direction or location.\n")
            return
        
        args = args.lower().strip()
        location = LOCATIONS.get(self.player.current_location)
        
        if args not in location.exits:
            print(f"\n❌ You can't go {args} from here.\n")
            print(f"Available exits: {', '.join(location.exits.keys())}\n")
            return
        
        new_location = location.exits[args]
        self.player.current_location = new_location
        self.game_state.visited_locations.add(new_location)
        print(f"\n✅ You move {args}...\n")
    
    def cmd_examine(self, args):
        """Examine command - look closely at something.
        
        Args:
            args: What to examine
        """
        if not args:
            print("\n❌ Examine what? Please specify.\n")
            return
        
        args = args.lower().strip()
        location = LOCATIONS.get(self.player.current_location)
        
        # Check items in location
        if args in [item.lower() for item in location.items]:
            self._examine_item(args)
            return
        
        # Check NPCs
        if args in [npc.lower() for npc in location.npcs]:
            self._examine_npc(args)
            return
        
        print(f"\n❌ You don't see '{args}' here.\n")
    
    def _examine_item(self, item):
        """Examine an item at current location.
        
        Args:
            item: Item name
        """
        examinations = {
            "notebook": "Your worn detective's notebook, filled with years of observations and cases.",
            "communication_device": "A sleek communication device. You can contact the station from here.",
            "case_files": "Official case files. They contain details about recent incidents in the city.",
            "forensic_evidence": "Evidence markers and biological samples. Whoever did this left traces.",
            "personal_effects": "Belongings of the victim. A wedding ring, a photo, personal mementos.",
            "citizen_records": "Vast databases of every citizen in the Caves. Where do you start?",
            "nutrition_pack": "Standard nutrition rations. Efficient, but utterly flavorless.",
        }
        
        examination = examinations.get(item, f"You examine the {item} carefully.")
        print(f"\n🔍 {examination}\n")
    
    def _examine_npc(self, npc):
        """Examine an NPC.
        
        Args:
            npc: NPC name
        """
        descriptions = {
            "r. daneel olivaw": "A humanoid robot with a smooth, plastic face and penetrating electronic eyes. Despite being a robot, there's something almost human about him.",
            "commissioner": "An imposing man in uniform, clearly uncomfortable about the robot partnership.",
            "desk officer": "A hardened veteran of the police force, weathered by years of service.",
            "commander": "A stern-faced woman who commands respect through presence alone.",
            "neighbor": "An ordinary citizen going about their daily life.",
            "city official": "A bureaucrat in formal attire, always busy with official business.",
            "street vendor": "Someone selling goods in the plaza, trying to make a living.",
            "administrator": "A professional, efficient and polite.",
            "records clerk": "A tired-looking person who has spent years managing data.",
            "dispensary attendant": "An employee mindlessly restocking nutrition dispensers.",
            "scene officer": "A forensic officer still collecting evidence.",
        }
        
        description = descriptions.get(npc.lower(), f"You observe {npc} carefully.")
        print(f"\n👤 {description}\n")
    
    def cmd_talk(self, args):
        """Talk command - speak to an NPC.
        
        Args:
            args: Who to talk to
        """
        if not args:
            print("\n❌ Talk to whom? Specify an NPC.\n")
            return
        
        args = args.lower().strip()
        location = LOCATIONS.get(self.player.current_location)
        
        if args not in [npc.lower() for npc in location.npcs]:
            print(f"\n❌ '{args}' isn't here.\n")
            return
        
        self._dialogue(args)
    
    def _dialogue(self, npc):
        """Handle dialogue with an NPC.
        
        Args:
            npc: NPC name (lowercase)
        """
        self.player.met_characters.add(npc)
        
        dialogues = {
            "r. daneel olivaw": """
        R. Daneel Olivaw regards you with those unblinking robotic eyes.
        
        "Good morning, Detective. I am R. Daneel Olivaw, a humanoid robot
        from the Outer Regions. I have been assigned as your partner in
        this investigation. I hope my presence will not be... problematic.
        I am designed to follow the Three Laws of Robotics, which ensures
        I will protect human life."
        
        How do you respond?
        """,
            "commissioner": """
        The Commissioner leans back in his chair, his face stern.
        
        "Listen here, detective. I know you're not happy about working
        with a robot. But the Outer Regions have demanded it. There's
        been a murder with political implications. We need to solve this
        quickly and carefully. The robot stays with you."
        
        He eyes you coldly. The matter is not up for discussion.
        """,
            "records clerk": """
        The clerk looks up from their work, exhausted.
        
        "Welcome to Records. Do you need citizen information? Birth records?
        Employment history? Everything about every person in these caves
        is filed here. It's all... so much data."
        
        What information do you seek?
        """,
        }
        
        dialogue = dialogues.get(npc, f"You talk with {npc}.")
        print(f"\n💬 {dialogue}\n")
    
    def cmd_inventory(self, args):
        """Inventory command - show what player is carrying."""
        print(f"\n📦 INVENTORY:\n")
        if not self.player.inventory:
            print("You're not carrying anything.\n")
            return
        
        for item, quantity in self.player.inventory.items():
            print(f"  • {item} x{quantity}")
        print()
    
    def cmd_take(self, args):
        """Take command - pick up an item or all items.
        
        Args:
            args: What to take (or "all")
        """
        if not args:
            print("\n❌ Take what? Please specify (or 'take all').\n")
            return
        
        args = args.lower().strip()
        location = LOCATIONS.get(self.player.current_location)
        
        if args == "all":
            if not location.items:
                print("\n❌ There are no items here to take.\n")
                return
            
            items_taken = []
            for item in location.items[:]:  # Create a copy to iterate safely
                self.player.add_item(item)
                items_taken.append(item)
            
            location.items.clear()
            items_str = ", ".join(items_taken)
            print(f"\n✅ You take all items: {items_str}.\n")
            return
        
        if args not in [item.lower() for item in location.items]:
            print(f"\n❌ You don't see '{args}' here.\n")
            return
        
        # Find the actual item name (with correct case)
        actual_item = next(item for item in location.items if item.lower() == args)
        self.player.add_item(actual_item)
        location.items.remove(actual_item)
        print(f"\n✅ You take the {actual_item}.\n")
    
    def cmd_drop(self, args):
        """Drop command - drop an item or all items from inventory.
        
        Args:
            args: What to drop (or "all")
        """
        if not args:
            print("\n❌ Drop what? Please specify (or 'drop all').\n")
            return
        
        args = args.lower().strip()
        
        if args == "all":
            if not self.player.inventory:
                print("\n❌ You're not carrying anything.\n")
                return
            
            items_dropped = []
            location = LOCATIONS.get(self.player.current_location)
            
            for item in list(self.player.inventory.keys()):
                quantity = self.player.inventory[item]
                location.items.append(item)
                items_dropped.append(f"{item} x{quantity}")
            
            self.player.inventory.clear()
            items_str = ", ".join(items_dropped)
            print(f"\n✅ You drop all items: {items_str}.\n")
            return
        
        if not self.player.has_item(args):
            print(f"\n❌ You don't have '{args}'.\n")
            return
        
        self.player.remove_item(args)
        location = LOCATIONS.get(self.player.current_location)
        location.items.append(args)
        print(f"\n✅ You drop the {args}.\n")
    
    def cmd_status(self, args):
        """Status command - show detailed player and game status."""
        print(self.player.get_status())
        print(self.game_state.get_summary())
        if self.player.clues_found:
            print("\n🔍 CLUES FOUND:")
            for i, clue in enumerate(self.player.clues_found, 1):
                print(f"   {i}. {clue}")
        print()
    
    def cmd_help(self, args):
        """Help command - show available commands."""
        help_text = """
        ╔════════════════════════════════════════════════════════════╗
        ║                   AVAILABLE COMMANDS                       ║
        ╠════════════════════════════════════════════════════════════╣
        ║ MOVEMENT:                                                  ║
        ║   go <direction>     Move to another location             ║
        ║                                                            ║
        ║ INTERACTION:                                               ║
        ║   look              Look around your surroundings         ║
        ║   examine <thing>   Examine an object or person          ║
        ║   talk <to person>  Speak with an NPC                    ║
        ║   take <item>       Pick up an item                      ║
        ║   take all          Pick up all items in location        ║
        ║   drop <item>       Drop an item from inventory          ║
        ║   drop all          Drop all items from inventory        ║
        ║                                                            ║
        ║ INVESTIGATION:                                             ║
        ║   mystery           Show mystery details                 ║
        ║   accuse <person>   Accuse someone of the murder         ║
        ║   relationships     Show NPC relationships               ║
        ║   puzzle <id>       Solve a puzzle (access_code, etc.)   ║
        ║                                                            ║
        ║ INFORMATION:                                               ║
        ║   inventory (i)     Show what you're carrying            ║
        ║   status            Show detective status & clues         ║
        ║   help              Show this help message                ║
        ║                                                            ║
        ║ SAVE/LOAD:                                                 ║
        ║   save (s)          Save your game progress              ║
        ║   load (l)          Load a previous save                 ║
        ║                                                            ║
        ║ GAME:                                                      ║
        ║   quit              Exit the game                         ║
        ╚════════════════════════════════════════════════════════════╝
        """
        print(help_text)
    
    def cmd_mystery(self, args):
        """Show mystery details and suspects."""
        print(self.game_state.mystery.get_mystery_summary())
        print("\n🕵️ SUSPECTS:\n")
        for suspect_name in self.game_state.mystery.suspects.keys():
            print(f"  • {suspect_name}")
        print()
    
    def cmd_accuse(self, args):
        """Accuse someone of the murder.
        
        Args:
            args: Name of person to accuse
        """
        if not args:
            print("\n❌ Accuse whom? Be specific.\n")
            return
        
        args = args.strip().title()
        
        # Check if they have enough evidence
        can_accuse, remaining = self.game_state.mystery.can_accuse(self.player)
        if not can_accuse:
            print(f"\n❌ You don't have enough evidence yet. You need {remaining} more clue(s).\n")
            return
        
        result = self.game_state.mystery.check_solution(args)
        
        if result["correct"]:
            print(f"\n✅ {result['message']}")
            print(f"Motive: {result['explanation']}\n")
            self.game_state.case_solved = True
        else:
            print(f"\n❌ {result['message']}")
            print(f"{result['explanation']}\n")
    
    def cmd_relationships(self, args):
        """Show relationships with all NPCs."""
        print(self.game_state.relationships.get_all_relationships())
    
    def cmd_puzzle(self, args):
        """Attempt to solve a puzzle or get hint.
        
        Args:
            args: Puzzle ID or answer
        """
        if not args:
            print("\n❌ Usage: puzzle <id> or solve <id> <answer>\n")
            solved, total = self.game_state.puzzle_manager.get_solved_puzzles()
            print(f"Puzzles solved: {solved}/{total}\n")
            return
        
        parts = args.split(maxsplit=1)
        puzzle_id = parts[0].lower()
        
        if len(parts) == 1:
            # Get hint
            hint = self.game_state.puzzle_manager.get_hint(puzzle_id)
            print(f"\n💡 Hint: {hint}\n")
        else:
            # Attempt solution
            answer = parts[1]
            result = self.game_state.puzzle_manager.solve_puzzle(puzzle_id, answer)
            
            if result["success"]:
                print(f"\n{result['message']}")
                self.player.investigation_points += result.get("reward", 0)
                print(f"Investigation points +{result.get('reward', 0)}!\n")
            else:
                print(f"\n{result['message']}\n")

