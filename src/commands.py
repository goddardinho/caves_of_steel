"""
Command Processor - Handles player commands
"""

from src.locations import LOCATIONS


# NPC name mappings for first-name shortcuts
NPC_NAME_MAP = {
    # Full names
    "r. daneel olivaw": "R. Daneel Olivaw",
    "daneel": "R. Daneel Olivaw",
    "r daneel": "R. Daneel Olivaw",
    "olivaw": "R. Daneel Olivaw",
    "julius enderby": "Julius Enderby",
    "julius": "Julius Enderby",
    "enderby": "Julius Enderby",
    "commissioner": "Julius Enderby",
    "records clerk": "Records Clerk",
    "clerk": "Records Clerk",
    "vince barrett": "Vince Barrett",
    "vince": "Vince Barrett",
    "barrett": "Vince Barrett",
    "r. sammy": "R. Sammy",
    "sammy": "R. Sammy",
    "r sammy": "R. Sammy",
    "han fastolfe": "Han Fastolfe",
    "han": "Han Fastolfe",
    "fastolfe": "Han Fastolfe",
    "dr. anthony gerrigel": "Dr. Anthony Gerrigel",
    "anthony": "Dr. Anthony Gerrigel",
    "gerrigel": "Dr. Anthony Gerrigel",
    "dr gerrigel": "Dr. Anthony Gerrigel",
    "francis clousarr": "Francis Clousarr",
    "francis": "Francis Clousarr",
    "clousarr": "Francis Clousarr",
    "commander lije bailey": "Commander Lije Bailey",
    "commander": "Commander Lije Bailey",
    "lije": "Commander Lije Bailey",
    "lije bailey": "Commander Lije Bailey",
    "jessie bailey": "Jessie Bailey",
    "jessie": "Jessie Bailey",
    "ben bailey": "Ben Bailey",
    "ben": "Ben Bailey",
    "bentley": "Ben Bailey",
}


class CommandProcessor:
    """Processes and executes player commands."""

    def __init__(self, player, game_state, demo_mode=False):
        """Initialize command processor.

        Args:
            player: Player object
            game_state: GameState object
            demo_mode: If True, skip input prompts and use defaults
        """
        self.player = player
        self.game_state = game_state
        self.demo_mode = demo_mode
        self.commands = {
            "look": self.cmd_look,
            "go": self.cmd_go,
            "move": self.cmd_go,
            "examine": self.cmd_examine,
            "inspect": self.cmd_examine,
            "talk": self.cmd_talk,
            "ask": self.cmd_ask,
            "play": self.cmd_play,
            "comfort": self.cmd_comfort,
            "speak": self.cmd_talk,
            "inventory": self.cmd_inventory,
            "inv": self.cmd_inventory,
            "i": self.cmd_inventory,
            "take": self.cmd_take,
            "get": self.cmd_take,
            "drop": self.cmd_drop,
            "status": self.cmd_status,
            "stats": self.cmd_stats,
            "help": self.cmd_help,
            "accuse": self.cmd_accuse,
            "investigate": self.cmd_investigate,
            "relationships": self.cmd_relationships,
            "mystery": self.cmd_mystery,
            "puzzle": self.cmd_puzzle,
            "settings": self.cmd_settings,
        }

    def _resolve_npc_name(self, input_name):
        """Resolve a player input NPC name to the canonical full name.

        Args:
            input_name: Player's input (e.g., "daneel", "han", "julius")

        Returns:
            str: Canonical NPC name, or the input if no match found
        """
        input_lower = input_name.lower().strip()
        return NPC_NAME_MAP.get(input_lower, input_name)

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
            print(
                f"\n❌ Unknown command: '{command}'. Type 'help' for available commands.\n"
            )

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
        if not location:
            print("\n❌ Current location data is missing. You cannot move right now.\n")
            return

        exits = getattr(location, "exits", {}) or {}
        if args not in exits:
            print(f"\n❌ You can't go {args} from here.\n")
            if exits:
                print(f"Available exits: {', '.join(exits.keys())}\n")
            else:
                print("There are no obvious exits from here.\n")
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
        if not location:
            print("\n❌ Current location data is missing. Nothing to examine here.\n")
            return

        loc_items = location.items or []
        loc_npcs = location.npcs or []

        # Check items in location
        if args in [item.lower() for item in loc_items]:
            self._examine_item(args)
            return

        # Check NPCs
        if args in [npc.lower() for npc in loc_npcs]:
            self._examine_npc(args)
            return

        # Check inventory (allow examining items you've picked up)
        if args in [item.lower() for item in self.player.inventory.keys()]:
            self._examine_item(args)
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
            "eyeglass_evidence": """A pair of eyeglasses in a repair case. The lenses are clearly broken — shattered 
in a pattern consistent with impact trauma. The metal frames show signs of stress. 
These glasses are definitely not new — they're being repaired. 
                
You notice fragments of glass that could be tested forensically. 
This might be connected to the crime scene.""",
        }

        examination = examinations.get(item, f"You examine the {item} carefully.")
        print(f"\n🔍 {examination}\n")

    def _examine_npc(self, npc):
        """Examine an NPC.

        Args:
            npc: NPC name (can be first name or full name)
        """
        # Resolve first name to full name
        canonical_npc = self._resolve_npc_name(npc)
        
        descriptions = {
            "r. daneel olivaw": "A humanoid robot with a smooth, plastic face and penetrating electronic eyes. Despite being a robot, there's something almost human about him.",
            "julius enderby": "The Commissioner — an imposing man in uniform with keen eyes. He commands authority and expects results.",
            "desk officer": "A hardened veteran of the police force, weathered by years of service.",
            "commander lije bailey": "A stern-faced officer who commands respect through presence alone.",
            "neighbor": "An ordinary citizen going about their daily life.",
            "city official": "A bureaucrat in formal attire, always busy with official business.",
            "street vendor": "Someone selling goods in the plaza, trying to make a living.",
            "administrator": "A professional, efficient and polite.",
            "records clerk": "A tired-looking person who has spent years managing data.",
            "dispensary attendant": "An employee mindlessly restocking nutrition dispensers.",
            "scene officer": "A forensic officer still collecting evidence.",
            "jessie bailey": "Jessie Bailey — your wife. Warm, practical, and quietly proud of your work. She worries about the long hours and keeps the household steady.",
            "ben bailey": "Ben Bailey — your young son. Energetic, curious, and fascinated by robots. He loves asking questions and getting distracted easily.",
            "vince barrett": "A junior officer with a bitter expression. He lost his position when robots were integrated into the department.",
            "r. sammy": "A service robot with efficient movements. His optical sensors track everything with mechanical precision.",
            "han fastolfe": "A well-dressed stranger with an air of quiet authority. He carries himself with the bearing of someone accustomed to spacer technology.",
            "dr. anthony gerrigel": "A distinguished scientist surrounded by robotics equipment and research data. His expression is thoughtful and measured.",
            "francis clousarr": "A thin, intense man behind detention glass. His eyes burn with conviction and resentment toward robots.",
        }

        description = descriptions.get(canonical_npc.lower(), f"You observe {canonical_npc} carefully.")
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
        if not location:
            print("\n❌ Current location data is missing. No one to talk to.\n")
            return

        loc_npcs = location.npcs or []
        if args not in [npc.lower() for npc in loc_npcs]:
            print(f"\n❌ '{args}' isn't here.\n")
            return

        self._dialogue(args)

    def _dialogue(self, npc):
        """Handle dialogue with an NPC.

        Args:
            npc: NPC name (lowercase, can be first name or full name)
        """
        # Resolve first name to full name
        canonical_npc = self._resolve_npc_name(npc)
        
        self.player.met_characters.add(canonical_npc)

        # Notify relationship manager (if available) that we talked to this NPC
        try:
            rel_manager = getattr(self.game_state, "relationships", None)
            if rel_manager:
                # Find the canonical NPC name in the relationships map (case-insensitive)
                match = next((k for k in rel_manager.relationships.keys() if k.lower() == canonical_npc.lower()), None)
                if match:
                    rel_manager.talk_to_npc(match)
        except Exception:
            pass

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
            "julius enderby": """
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
            "vince barrett": """
        Vince looks at you with barely concealed frustration.
        
        "Another investigation where the robots get all the attention, huh?
        Used to be, we did the real work. Now they show up and take credit
        for the deductions. Just watch — that Daneel will solve it and
        we'll all look bad for needing the help."
        
        He turns away bitterly.
        """,
            "r. sammy": """
        R. Sammy's optical sensors pulse with pale blue light.
        
        "Detective. My data analysis is complete. Dr. Roj Nemennuh Sarton
        was a significant figure in robotics research. The circumstances
        of his death suggest involvement by someone with motive and opportunity.
        I stand ready to assist in deductive analysis."
        
        The robot speaks with mechanical precision.
        """,
            "han fastolfe": """
        Han regards you with composed interest.
        
        "Detective. I knew of Roj Sarton through his published research.
        He was attempting something ambitious — proving that humans and robots
        could work together seamlessly. His death is a tragedy for that vision.
        I wonder if someone feared what his success might mean."
        
        He pauses meaningfully.
        """,
            "dr. anthony gerrigel": """
        Dr. Gerrigel looks up from his workstation, concern in his eyes.
        
        "Roj and I collaborated frequently. He was exploring questions about
        robot consciousness and human-robot partnership. His latest work...
        it was groundbreaking. Perhaps too groundbreaking for some people."
        
        He adjusts his glasses thoughtfully.
        """,
            "francis clousarr": """
        Francis leans forward, his voice sharp and bitter.
        
        "You want to know if I did it? I didn't. But I'm glad he's dead.
        Sarton spent his life making machines that take human jobs, human lives,
        human dignity. Maybe someone else agreed with me more forcefully."
        
        His fists clench against the detention glass.
        """,
            "commander lije bailey": """
        The Commander reviews a file on his desk, then looks up.
        
        "Good to see you. The Sarton case is priority. We've got pressure
        from above — the Outer Regions, the Commissioner, everyone. You and
        that robot partner of yours need to bring this to a close. Fast.
        Any leads?"
        
        He waits for your response.
        """,
            "jessie bailey": """
        Jessie looks up from a small pile of personal effects, smiling when she sees you.

        "Hello, love," she says softly. "Are you all right? You look tired. Don't forget we have dinner at seven — Ben has been asking about your robot partner."

        She reaches for your hand, steady and familiar. "Be careful out there."

        """,
            "ben bailey": """
        Ben bounces in place, eyes wide with curiosity.

        "Is that the robot?" he asks, pointing toward R. Daneel. "Can I see how it walks? Can it play with me?"

        He fidgets, then leans in conspiratorially: "Do robots eat?"

        """,
        }

        dialogue = dialogues.get(npc, f"You talk with {npc}.")
        # Replace address 'Detective' with the player's actual name for immersion
        try:
            pname = self.player.name
        except Exception:
            pname = "Detective"
        dialogue = dialogue.replace("Detective", pname).replace("detective", pname)
        print(f"\n💬 {dialogue}\n")

        # Branching dialogue for family members
        try:
            if npc.lower() == "jessie bailey":
                # Present simple choice menu
                print("\nOptions: 1) Reassure Jessie  2) Ask about dinner  3) Say goodbye\n")
                if self.demo_mode:
                    choice = "1"  # Default choice in demo mode
                else:
                    try:
                        choice = input("Choose an option (1-3): ").strip()
                    except Exception:
                        choice = "1"

                if choice == "1":
                    print("\nYou reassure Jessie that you'll be careful. She seems calmer.\n")
                    try:
                        self.game_state.relationships.get_relationship("Jessie Bailey").increase_trust(5)
                    except Exception:
                        pass
                elif choice == "2":
                    print("\nYou ask about dinner. Jessie confirms and smiles.\n")
                else:
                    print("\nYou exchange a quiet word and leave.\n")

            elif npc.lower() == "ben bailey":
                print("\nOptions: 1) Play with Ben  2) Answer about robots  3) Send him to his room\n")
                if self.demo_mode:
                    choice = "1"  # Default choice in demo mode
                else:
                    try:
                        choice = input("Choose an option (1-3): ").strip()
                    except Exception:
                        choice = "1"

                if choice == "1":
                    print("\nYou play a quick game with Ben. His laughter fills the room.\n")
                    try:
                        self.game_state.relationships.get_relationship("Ben Bailey").increase_trust(7)
                    except Exception:
                        pass
                elif choice == "2":
                    print("\nYou explain briefly that robots don't eat like people; Ben is fascinated.\n")
                else:
                    print("\nYou send Ben off to play quietly; he stamps away reluctantly.\n")
        except Exception:
            pass

    def cmd_inventory(self, args):
        """Inventory command - show what player is carrying."""
        print("\n📦 INVENTORY:\n")
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
        if not location:
            print(
                "\n❌ Current location data is missing. You can't take items right now.\n"
            )
            return

        loc_items = location.items or []

        if args == "all":
            if not loc_items:
                print("\n❌ There are no items here to take.\n")
                return

            items_taken = []
            for item in list(loc_items):  # Create a copy to iterate safely
                self.player.add_item(item)
                items_taken.append(item)

            # Clear stored items on the location (ensure list exists)
            if location.items is None:
                location.items = []
            else:
                location.items.clear()

            items_str = ", ".join(items_taken)
            print(f"\n✅ You take all items: {items_str}.\n")
            return

        if args not in [item.lower() for item in loc_items]:
            print(f"\n❌ You don't see '{args}' here.\n")
            return

        # Find the actual item name (with correct case)
        actual_item = next(item for item in loc_items if item.lower() == args)
        self.player.add_item(actual_item)
        # Remove from the underlying location.items if present
        if location.items is None:
            location.items = []
        if actual_item in location.items:
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
            if not location:
                print(
                    "\n❌ Current location data is missing. You can't drop items here.\n"
                )
                return

            if location.items is None:
                location.items = []

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
        if not location:
            print(
                "\n❌ Current location data is missing. Dropped item lost to the void.\n"
            )
            return

        if location.items is None:
            location.items = []

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

    def cmd_stats(self, args):
        """Stats command - show quick statistics."""
        print("\n" + "=" * 50)
        print("QUICK STATS")
        print("=" * 50)
        print(f"Detective: {self.player.name}")
        print(f"Difficulty: {self.player.difficulty.capitalize()}")
        print(f"Investigation Points: {self.player.investigation_points}")
        print(f"Clues Found: {len(self.player.clues_found)}")
        print(f"Energy Level: {self.player.energy}%")
        print(
            f"Day: {self.game_state.day} - {self.game_state.time_period.capitalize()}"
        )
        print(f"Locations Visited: {len(self.game_state.visited_locations)}")
        print("=" * 50 + "\n")

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
        ║   stats             Show quick statistics                ║
        ║   help              Show this help message                ║
        ║                                                            ║
        ║ SETTINGS:                                                  ║
        ║   settings          Open settings menu                   ║
        ║   settings name     Change your detective name           ║
        ║ FAMILY:                                                    ║
        ║   ask <npc> <topic>   Ask an NPC about a topic (family-only) ║
        ║   play <npc>          Play with a child NPC (Ben)           ║
        ║   comfort <npc>       Comfort a worried family member (Jessie) ║
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

    def cmd_ask(self, args):
        """Ask command - ask an NPC about a topic (family-focused)

        Args:
            args: "<npc> <topic>"
        """
        if not args:
            print("\n❌ Usage: ask <npc> <topic>\n")
            return

        parts = args.split(maxsplit=1)
        npc_input = parts[0].lower()
        canonical_npc = self._resolve_npc_name(npc_input)
        topic = parts[1].lower() if len(parts) > 1 else ""

        # Family-specific topics
        if canonical_npc.lower() in ("jessie bailey",):
            if "dinner" in topic or "meal" in topic:
                print("\n💬 Jessie: 'Yes — dinner at seven. Ben is excited.'\n")
                try:
                    self.game_state.relationships.get_relationship("Jessie Bailey").increase_trust(3)
                except Exception:
                    pass
                return
            print("\n💬 Jessie: 'I'm busy right now, love. Later?'\n")
            return

        if canonical_npc.lower() in ("ben bailey",):
            if "robot" in topic:
                print("\n💬 Ben: 'Robots are cool! They can walk and talk.'\n")
                try:
                    self.game_state.relationships.get_relationship("Ben Bailey").increase_trust(2)
                except Exception:
                    pass
                return
            print("\n💬 Ben: 'I dunno about that. Can we play instead?'\n")
            return

        print(f"\n❌ You can't ask '{canonical_npc}' about that here.\n")

    def cmd_play(self, args):
        """Play command - play with a child NPC (Ben)."""
        if not args:
            print("\n❌ Play with whom? Try: play ben\n")
            return

        npc_input = args.lower().strip()
        canonical_npc = self._resolve_npc_name(npc_input)
        
        if canonical_npc.lower() in ("ben bailey",):
            print("\n🎲 You play a quick game with Ben. He laughs and tugs your sleeve.\n")
            try:
                self.game_state.relationships.get_relationship("Ben Bailey").increase_trust(10)
            except Exception:
                pass
            return

        print("\n❌ You can't play with that NPC.\n")

    def cmd_comfort(self, args):
        """Comfort command - comfort a worried family member (Jessie)."""
        if not args:
            print("\n❌ Comfort whom? Try: comfort jessie\n")
            return

        npc_input = args.lower().strip()
        canonical_npc = self._resolve_npc_name(npc_input)
        
        if canonical_npc.lower() in ("jessie bailey",):
            print("\n🤝 You take Jessie in a brief embrace and assure her you'll be careful.\n")
            try:
                self.game_state.relationships.get_relationship("Jessie Bailey").increase_trust(8)
            except Exception:
                pass
            return

        print("\n❌ That action isn't appropriate for that NPC.\n")

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
            print(
                f"\n❌ You don't have enough evidence yet. You need {remaining} more clue(s).\n"
            )
            return

        result = self.game_state.mystery.check_solution(args)

        if result["correct"]:
            print(f"\n✅ {result['message']}")
            print(f"Motive: {result['explanation']}\n")
            self.game_state.case_solved = True
        else:
            print(f"\n❌ {result['message']}")
            print(f"{result['explanation']}\n")

    def cmd_investigate(self, args):
        """Investigate clue or evidence.

        Args:
            args: What to investigate (eyeglasses, enderby, spacer_conspiracy, etc.)
        """
        if not args:
            print("\n💡 You can investigate: eyeglasses, enderby, sammy, spacer_conspiracy\n")
            return

        investigation = args.lower().strip()

        # Eyeglass evidence investigation
        if investigation == "eyeglasses":
            if "eyeglass_evidence" in self.player.inventory:
                print("""
                ╔═ FORENSIC ANALYSIS ═╗
                You examine the broken eyeglasses closely.
                
                The fracture pattern suggests they were dropped or impacted forcefully.
                Fragments match those found at the crime scene in Spacetown.
                
                These glasses belong to someone with significant authority — 
                they're custom-made, expensive, not standard issue.
                
                ✅ EVIDENCE RECORDED: Eyeglass fragments match crime scene.
                """)
                self.game_state.mystery.record_evidence("broken_glasses_found")
            else:
                print("\n❌ You don't have eyeglass evidence.\n")

        # Enderby investigation
        elif investigation == "enderby":
            print("""
            ╔═ DEDUCTIVE ANALYSIS ═╗
            
            Commissioner Julius Enderby has been acting nervously.
            He compulsively adjusts his eyeglasses.
            His alibi places him in his office, but no one independently confirms this.
            
            He has access to all police facilities and resources.
            He could easily arrange for evidence disposal.
            
            Most notably: broken eyeglasses were in his office repair case.
            
            ✅ EVIDENCE RECORDED: Enderby's suspicious behavior and broken glasses.
            """)
            self.game_state.mystery.record_evidence("enderby_medievalist")

        # R. Sammy investigation
        elif investigation == "sammy":
            print("""
            ╔═ ROBOT ANALYSIS ═╗
            
            R. Sammy was present in the station but claims limited activity.
            Under First Law, R. Sammy could not directly harm a human.
            However, R. Sammy could follow orders to transport objects.
            
            If R. Sammy transported a blaster to Spacetown at someone's request,
            that someone must have had authority over the robot.
            
            Only a high-ranking official could command R. Sammy.
            
            ✅ EVIDENCE RECORDED: R. Sammy involvement as accomplice.
            """)
            self.game_state.mystery.record_evidence("r_sammy_transport")

        # Spacer conspiracy investigation
        elif investigation == "spacer_conspiracy":
            print("""
            ╔═ CONSPIRACY ANALYSIS ═╗
            
            The Spacers arrived on Earth to promote human-robot cooperation.
            Dr. Sarton was a key figure in this effort.
            Yet the Spacers seem oddly unconcerned about his death.
            
            Could Sarton's death have been... beneficial to their goals?
            A martyred proponent of human-robot partnership might inspire more converts.
            
            The Spacers accepted the murder as a 'necessary sacrifice.'
            
            This suggests:
            - They knew more than they revealed
            - The real target was R. Daneel, not Sarton
            - An anti-robot faction wanted to kill the robot, not the scientist
            
            ✅ EVIDENCE RECORDED: Spacer conspiracy and mistaken identity theory.
            """)
            self.game_state.mystery.record_evidence("spacer_conspiracy")

        else:
            print(f"\n❌ Cannot investigate '{investigation}'. Unknown topic.\n")

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

    def cmd_settings(self, args):
        """Settings command - view and manage game settings."""
        print("\n" + "=" * 50)
        print("GAME SETTINGS")
        print("=" * 50)
        print(f"\nPlayer Name: {self.player.name}")
        print(f"Difficulty: {self.player.difficulty.capitalize()}")
        print("\nAvailable options:")
        print("  settings name <new_name> - Change your detective name")
        print("  settings show            - Show all settings")
        print("  settings close           - Close settings menu\n")

        if args:
            parts = args.split(maxsplit=1)
            option = parts[0].lower()

            if option == "name" and len(parts) > 1:
                new_name = parts[1]
                if len(new_name) > 30:
                    print("❌ Name too long (max 30 characters)\n")
                else:
                    old_name = self.player.name
                    self.player.name = new_name
                    print(
                        f"✓ Detective name changed from '{old_name}' to '{new_name}'\n"
                    )
            elif option == "show":
                print("\n📋 CURRENT GAME SETTINGS:")
                print(f"  Detective Name: {self.player.name}")
                print(f"  Difficulty Level: {self.player.difficulty.capitalize()}")
                print(f"  Current Location: {self.player.current_location}")
                print(f"  Investigation Points: {self.player.investigation_points}")
                print(f"  Energy: {self.player.energy}%")
                print(f"  Day: {self.game_state.day}")
                print(f"  Time of Day: {self.game_state.time_period.capitalize()}\n")
            elif option == "close":
                print("Closing settings menu.\n")
            else:
                print("❌ Unknown settings option.\n")
