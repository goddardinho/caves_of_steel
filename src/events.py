"""
Time-Based Events System - Events that trigger at specific times
"""


class TimedEvent:
    """Represents an event that occurs at a specific game time."""
    
    def __init__(self, event_id, description, time_period, day, action=None):
        """Initialize a timed event.
        
        Args:
            event_id: Unique event ID
            description: What happens
            time_period: When it happens (morning, afternoon, evening, night)
            day: Which day (1, 2, 3, etc.)
            action: Function to call when event triggers
        """
        self.event_id = event_id
        self.description = description
        self.time_period = time_period
        self.day = day
        self.action = action
        self.triggered = False
    
    def should_trigger(self, current_day, current_time):
        """Check if this event should trigger.
        
        Args:
            current_day: Current game day
            current_time: Current time period
            
        Returns:
            bool: Whether event should trigger
        """
        return (current_day == self.day and 
                current_time == self.time_period and 
                not self.triggered)


class EventManager:
    """Manages all timed events in the game."""
    
    def __init__(self):
        """Initialize event manager."""
        self.events = []
        self._create_events()
        self.events_log = []
    
    def _create_events(self):
        """Create all timed events."""
        # Day 1 Events
        self.events.append(TimedEvent(
            "murder_discovery",
            "You receive urgent notification: Dr. Rimbauer has been found dead!",
            "morning",
            1
        ))
        
        self.events.append(TimedEvent(
            "partner_assignment",
            "R. Daneel Olivaw arrives at the Police Headquarters.",
            "afternoon",
            1
        ))
        
        self.events.append(TimedEvent(
            "first_lead",
            "A witness comes forward with information about seeing someone enter Rimbauer's apartment.",
            "evening",
            1
        ))
        
        # Day 2 Events
        self.events.append(TimedEvent(
            "suspect_meeting",
            "One of the suspects tries to contact you privately.",
            "morning",
            2
        ))
        
        self.events.append(TimedEvent(
            "evidence_found",
            "The forensics team reports finding additional evidence at the crime scene.",
            "afternoon",
            2
        ))
        
        self.events.append(TimedEvent(
            "conspiracy_hint",
            "You receive an anonymous message: 'The robots are involved. Rimbauer discovered something dangerous.'",
            "evening",
            2
        ))
        
        # Day 3 Events
        self.events.append(TimedEvent(
            "time_pressure",
            "The Commissioner calls: 'We need to wrap this up. You have until tomorrow morning.'",
            "morning",
            3
        ))
        
        self.events.append(TimedEvent(
            "breakthrough",
            "You finally piece together the evidence. You now understand who committed the murder.",
            "afternoon",
            3
        ))
        
        self.events.append(TimedEvent(
            "final_confrontation",
            "You're ready to confront the killer. This is your last chance.",
            "evening",
            3
        ))
    
    def get_triggered_events(self, current_day, current_time):
        """Get all events that should trigger now.
        
        Args:
            current_day: Current game day
            current_time: Current time period
            
        Returns:
            list: Events that should trigger
        """
        triggered = []
        for event in self.events:
            if event.should_trigger(current_day, current_time):
                event.triggered = True
                triggered.append(event)
                self.events_log.append(event.event_id)
        
        return triggered
    
    def display_event(self, event):
        """Display an event to the player.
        
        Args:
            event: TimedEvent to display
            
        Returns:
            str: Formatted event display
        """
        return f"""
        ╔═══════════════════════════════════════════╗
        ║              ** EVENT **                  ║
        ╠═══════════════════════════════════════════╣
        ║ {event.description}
        ╚═══════════════════════════════════════════╝
        """
    
    def has_event_occurred(self, event_id):
        """Check if a specific event has occurred.
        
        Args:
            event_id: Event ID to check
            
        Returns:
            bool: Whether event has been triggered
        """
        return event_id in self.events_log
    
    def get_events_log(self):
        """Get a summary of all events that have occurred.
        
        Returns:
            str: Formatted event log
        """
        if not self.events_log:
            return "No events have occurred yet."
        
        log = "📋 EVENT LOG:\n"
        for event_id in self.events_log:
            event = next((e for e in self.events if e.event_id == event_id), None)
            if event:
                log += f"  • {event.description}\n"
        
        return log
