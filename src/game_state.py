"""
GameState class - Tracks the state of the game world
"""

from src.mystery_plot import MysteryPlot
from src.relationships import RelationshipManager
from src.events import EventManager
from src.endings import EndingsManager
from src.puzzles import PuzzleManager
from src.dialogue_system import DialogueManager


class GameState:
    """Manages the overall state of the game world."""

    def __init__(self, difficulty="normal"):
        """Initialize game state.

        Args:
            difficulty: Game difficulty (easy, normal, hard)
        """
        self.difficulty = difficulty
        self.time_period = "morning"  # morning, afternoon, evening, night
        self.day = 1
        self.case_solved = False
        self.partner_assigned = False
        self.partner_name = "R. Daneel Olivaw"

        # World events
        self.events_triggered = set()
        self.npc_states = {}  # Track NPC-specific states
        self.visited_locations = set()

        # Initialize major systems
        self.mystery = MysteryPlot()
        self.relationships = RelationshipManager()
        self.event_manager = EventManager()
        self.endings_manager = EndingsManager()
        self.puzzle_manager = PuzzleManager()
        self.dialogue_manager = DialogueManager()

    def trigger_event(self, event_name):
        """Trigger a game event.

        Args:
            event_name: Name of the event to trigger
        """
        self.events_triggered.add(event_name)

    def is_event_triggered(self, event_name):
        """Check if an event has been triggered.

        Args:
            event_name: Name of the event

        Returns:
            bool: True if event has been triggered
        """
        return event_name in self.events_triggered

    def set_npc_state(self, npc_name, state_key, value):
        """Set state for an NPC.

        Args:
            npc_name: NPC name
            state_key: State key
            value: State value
        """
        if npc_name not in self.npc_states:
            self.npc_states[npc_name] = {}
        self.npc_states[npc_name][state_key] = value

    def get_npc_state(self, npc_name, state_key, default=None):
        """Get state for an NPC.

        Args:
            npc_name: NPC name
            state_key: State key
            default: Default value if not found

        Returns:
            State value or default
        """
        if npc_name not in self.npc_states:
            return default
        return self.npc_states[npc_name].get(state_key, default)

    def advance_time(self):
        """Advance time in the game."""
        periods = ["morning", "afternoon", "evening", "night"]
        current_index = periods.index(self.time_period)

        if current_index == 3:  # night -> morning of next day
            self.day += 1
            self.time_period = "morning"
        else:
            self.time_period = periods[current_index + 1]

    def get_summary(self):
        """Get a summary of the current game state.

        Returns:
            str: Formatted state summary
        """
        summary = f"""
        ┌─ GAME STATE ───────────────────────────┐
        │ Day: {self.day} ({self.time_period.capitalize()})
        │ Case Solved: {'Yes' if self.case_solved else 'No'}
        │ Partner Assigned: {'Yes' if self.partner_assigned else 'No'}
        │ Events Triggered: {len(self.events_triggered)}
        └────────────────────────────────────────┘
        """
        return summary
