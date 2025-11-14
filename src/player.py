"""
Player class - Represents the player character
"""


class Player:
    """Represents the player character."""
    
    def __init__(self, name, starting_location, difficulty="normal"):
        """Initialize the player.
        
        Args:
            name: Player's name
            starting_location: Starting location key
            difficulty: Game difficulty (easy, normal, hard)
        """
        self.name = name
        self.current_location = starting_location
        self.difficulty = difficulty
        self.inventory = {}
        self.energy = 100
        self.investigation_points = 0
        self.met_characters = set()
        self.clues_found = []
    
    def add_item(self, item, quantity=1):
        """Add item to inventory.
        
        Args:
            item: Item name
            quantity: Quantity to add
        """
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
    
    def remove_item(self, item, quantity=1):
        """Remove item from inventory.
        
        Args:
            item: Item name
            quantity: Quantity to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        if item not in self.inventory:
            return False
        
        if self.inventory[item] <= quantity:
            del self.inventory[item]
        else:
            self.inventory[item] -= quantity
        
        return True
    
    def has_item(self, item):
        """Check if player has an item.
        
        Args:
            item: Item name
            
        Returns:
            bool: True if player has item
        """
        return item in self.inventory and self.inventory[item] > 0
    
    def add_clue(self, clue):
        """Record a clue found during investigation.
        
        Args:
            clue: Clue description
        """
        if clue not in self.clues_found:
            self.clues_found.append(clue)
            self.investigation_points += 10
    
    def get_status(self):
        """Get player status as a formatted string.
        
        Returns:
            str: Player status
        """
        status = f"""
        ┌─ DETECTIVE STATUS ─────────────────────┐
        │ Name: {self.name}
        │ Difficulty: {self.difficulty.capitalize()}
        │ Location: {self.current_location}
        │ Energy: {self.energy}%
        │ Investigation Points: {self.investigation_points}
        │ Clues Found: {len(self.clues_found)}
        └────────────────────────────────────────┘
        """
        return status
