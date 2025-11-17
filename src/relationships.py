"""
NPC Relationship System - Track relationships with characters
"""


class NPCRelationship:
    """Tracks relationship with a single NPC."""

    def __init__(self, name):
        """Initialize NPC relationship.

        Args:
            name: NPC name
        """
        self.name = name
        self.trust = 0  # -100 to 100
        self.times_talked = 0
        self.times_helped = 0
        self.times_betrayed = 0
        self.likes_detective = True

    def increase_trust(self, amount):
        """Increase relationship trust.

        Args:
            amount: Amount to increase (capped at 100)
        """
        self.trust = min(100, self.trust + amount)

    def decrease_trust(self, amount):
        """Decrease relationship trust.

        Args:
            amount: Amount to decrease (minimum -100)
        """
        self.trust = max(-100, self.trust - amount)

    def add_dialogue(self):
        """Track that we've talked to this NPC."""
        self.times_talked += 1

    def help_npc(self):
        """Track that we helped this NPC."""
        self.times_helped += 1
        self.increase_trust(20)

    def betray_npc(self):
        """Track that we betrayed this NPC."""
        self.times_betrayed += 1
        self.decrease_trust(30)

    def get_relationship_status(self):
        """Get the relationship status as text.

        Returns:
            str: Relationship status (Hostile, Neutral, Friendly, etc.)
        """
        if self.trust >= 75:
            return "Ally"
        elif self.trust >= 50:
            return "Friendly"
        elif self.trust >= 25:
            return "Warm"
        elif self.trust >= 0:
            return "Neutral"
        elif self.trust >= -25:
            return "Wary"
        elif self.trust >= -50:
            return "Hostile"
        else:
            return "Enemy"


class RelationshipManager:
    """Manages relationships with all NPCs."""

    def __init__(self):
        """Initialize relationship manager."""
        self.relationships = {}
        self._init_npcs()

    def _init_npcs(self):
        """Initialize all NPC relationships."""
        npcs = [
            "Julius Enderby",
            "R. Daneel Olivaw",
            "Desk Officer",
            "Commander Lije Bailey",
            "Neighbor",
            "City Official",
            "Street Vendor",
            "Administrator",
            "Records Clerk",
            "Dispensary Attendant",
            "Jessie Bailey",
            "Ben Bailey",
            "Vince Barrett",
            "R. Sammy",
            "Han Fastolfe",
            "Dr. Anthony Gerrigel",
            "Francis Clousarr",
        ]

        for npc in npcs:
            self.relationships[npc] = NPCRelationship(npc)

        # Set initial family relationships warmer than default
        if "Jessie Bailey" in self.relationships:
            self.relationships["Jessie Bailey"].trust = 70
        if "Ben Bailey" in self.relationships:
            self.relationships["Ben Bailey"].trust = 50

    def get_relationship(self, npc_name):
        """Get relationship object for an NPC.

        Args:
            npc_name: NPC name

        Returns:
            NPCRelationship or None
        """
        return self.relationships.get(npc_name)

    def talk_to_npc(self, npc_name):
        """Record talking to an NPC.

        Args:
            npc_name: NPC name
        """
        rel = self.get_relationship(npc_name)
        if rel:
            rel.add_dialogue()
            rel.increase_trust(5)

    def get_all_relationships(self):
        """Get formatted summary of all relationships.

        Returns:
            str: Formatted relationships
        """
        summary = "\n┌─ NPC RELATIONSHIPS ────────────────────┐\n"

        for npc_name, rel in sorted(self.relationships.items()):
            status = rel.get_relationship_status()
            summary += f"│ {npc_name:<25} {status:>10} ({rel.trust:+3})\n"

        summary += "└────────────────────────────────────────┘\n"
        return summary

    def can_convince_npc(self, npc_name):
        """Check if NPC will cooperate based on relationship.

        Args:
            npc_name: NPC name

        Returns:
            bool: Whether NPC will help
        """
        rel = self.get_relationship(npc_name)
        return rel and rel.trust >= -25
