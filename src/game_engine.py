"""
Game Engine - Core loop and command processing
"""

from src.locations import LOCATIONS
from src.commands import CommandProcessor
from src.utils import clear_screen, print_separator
from src.save_system import SaveSystem


class GameEngine:
    """Main game engine that handles the core game loop."""

    def __init__(self, player, game_state, save_dir=None):
        """Initialize the game engine.

        Args:
            player: Player object
            game_state: GameState object
            save_dir: Optional custom save directory path
        """
        self.player = player
        self.game_state = game_state
        self.command_processor = CommandProcessor(player, game_state)
        self.save_system = SaveSystem(save_dir)
        self.running = True

    def run(self):
        """Main game loop."""
        self.display_welcome()

        # Trigger initial events
        self._check_for_events()

        while self.running:
            try:
                self.display_current_location()
                command = self.get_player_input()

                if command.lower() in ["quit", "exit", "q"]:
                    self.quit_game()
                    break

                if command.lower() in ["save", "s"]:
                    self.save_game()
                    continue

                if command.lower() in ["load", "l"]:
                    self.load_game()
                    continue

                self.command_processor.process(command)

                # Check if case is solved
                if self.game_state.case_solved:
                    self.display_case_conclusion()
                    break

                # Check for time events (every few turns advance time)
                # This happens after player actions
                self._check_for_events()

            except KeyboardInterrupt:
                print("\n\nGame interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try another command.\n")

    def run_demo(self, commands):
        """Run a scripted demo using a list of command strings.

        Args:
            commands: List[str] commands to run in sequence
        """
        # Minimal non-blocking welcome
        try:
            from src.utils import clear_screen

            clear_screen()
        except Exception:
            pass

        print("\n" + "=" * 60)
        print("THE CAVES OF STEEL - DEMO")
        print("A scripted demo showing basic game flow")
        print("=" * 60 + "\n")

        # Trigger initial events
        self._check_for_events()

        for cmd in commands:
            # Show location and run command
            self.display_current_location()
            print(f"\n> (demo) {cmd}\n")
            try:
                if cmd.lower() in ["quit", "exit", "q"]:
                    self.quit_game()
                    break

                if cmd.lower() in ["save", "s"]:
                    self.save_game()
                    continue

                if cmd.lower() in ["load", "l"]:
                    self.load_game()
                    continue

                self.command_processor.process(cmd)
                if self.game_state.case_solved:
                    self.display_case_conclusion()
                    break

                self._check_for_events()
            except Exception as e:
                print(f"Demo error: {e}")

    def display_welcome(self):
        """Display welcome message and initial scene."""
        clear_screen()
        print(
            """
        ╔════════════════════════════════════════════════════════════╗
        ║          THE CAVES OF STEEL - A Text Adventure             ║
        ║                                                            ║
        ║  You are a detective in New York City, year 4956 AD.      ║
        ║  Humanity lives in sprawling underground cave cities.      ║
        ║  A murder has been committed, and you must solve it.      ║
        ║  An unusual robot will be assigned as your partner.       ║
        ║                                                            ║
        ║  Commands: look, go [location], talk [to person],        ║
        ║           examine [object], inventory, help, quit         ║
        ╚════════════════════════════════════════════════════════════╝
        """
        )
        input("Press Enter to begin...")
        clear_screen()

    def display_current_location(self):
        """Display information about the current location."""
        location = LOCATIONS.get(self.player.current_location)
        if not location:
            print(f"ERROR: Unknown location '{self.player.current_location}'")
            return

        print_separator()
        print(f"\n📍 {location.name.upper()}\n")
        print(location.description)

        if location.exits:
            print(f"\n🚪 Exits: {', '.join(location.exits.keys())}")

        if location.npcs:
            print(f"\n👤 People: {', '.join(location.npcs)}")

        if location.items:
            print(f"\n📦 Items: {', '.join(location.items)}")

        print()

    def get_player_input(self):
        """Get and return player input."""
        try:
            return input("🎮 > ").strip()
        except EOFError:
            return "quit"

    def save_game(self):
        """Save the current game progress."""
        print("\n💾 Saving game...")
        save_path = self.save_system.save_game(self.player, self.game_state)
        print(f"✅ Game saved to: {save_path}\n")

    def load_game(self):
        """Load a saved game."""
        print("\n📂 Available saves:\n")
        saves = self.save_system.list_saves()

        if not saves:
            print("❌ No save files found.\n")
            return

        for i, (filename, timestamp) in enumerate(saves, 1):
            print(f"  {i}. {filename} ({timestamp})")

        print()
        try:
            choice = input(
                "Enter save number to load (or press Enter to cancel): "
            ).strip()
            if not choice:
                return

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(saves):
                filename = saves[choice_idx][0]
                player_data, game_state_data = self.save_system.load_game(filename)

                if player_data and game_state_data:
                    self._restore_player(player_data)
                    self._restore_game_state(game_state_data)
                    print(f"✅ Game loaded from: {filename}\n")
                else:
                    print("❌ Failed to load game.\n")
            else:
                print("❌ Invalid selection.\n")
        except ValueError:
            print("❌ Invalid input.\n")

    def _restore_player(self, player_data):
        """Restore player state from save data.

        Args:
            player_data: Dictionary of player data
        """
        self.player.current_location = player_data["current_location"]
        self.player.inventory = player_data["inventory"]
        self.player.energy = player_data["energy"]
        self.player.investigation_points = player_data["investigation_points"]
        self.player.met_characters = set(player_data["met_characters"])
        self.player.clues_found = player_data["clues_found"]

    def _restore_game_state(self, game_state_data):
        """Restore game state from save data.

        Args:
            game_state_data: Dictionary of game state data
        """
        self.game_state.time_period = game_state_data["time_period"]
        self.game_state.day = game_state_data["day"]
        self.game_state.case_solved = game_state_data["case_solved"]
        self.game_state.partner_assigned = game_state_data["partner_assigned"]
        self.game_state.partner_name = game_state_data["partner_name"]
        self.game_state.events_triggered = set(game_state_data["events_triggered"])
        self.game_state.visited_locations = set(game_state_data["visited_locations"])
        self.game_state.npc_states = game_state_data["npc_states"]

    def _check_for_events(self):
        """Check and display any triggered events."""
        events = self.game_state.event_manager.get_triggered_events(
            self.game_state.day, self.game_state.time_period
        )

        for event in events:
            print(self.game_state.event_manager.display_event(event))

            # Specific event handling
            if event.event_id == "murder_discovery":
                self.player.add_clue(
                    "Dr. Roj Nemennuh Sarton, a robotics specialist, has been murdered"
                )
            elif event.event_id == "partner_assignment":
                self.game_state.partner_assigned = True
                self.player.add_clue("Assigned humanoid robot partner R. Daneel Olivaw")
            elif event.event_id == "time_pressure":
                self.player.energy = max(0, self.player.energy - 20)

    def display_case_conclusion(self):
        """Display the case conclusion and ending."""
        ending = self.game_state.endings_manager.check_ending(
            self.player, self.game_state, self.game_state.mystery
        )

        if ending:
            print(self.game_state.endings_manager.display_ending(ending, self.player))
        else:
            print("\n❌ Case could not be resolved properly.\n")

        self.running = False

    def quit_game(self):
        """Handle game quit."""
        print("\nThank you for playing The Caves of Steel!")
        try:
            name = self.player.name
        except Exception:
            name = "Detective"
        print(f"Goodbye, {name}.\n")
        self.running = False
