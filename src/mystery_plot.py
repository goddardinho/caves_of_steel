"""
Mystery Plot System - Complete murder mystery with suspects and motives
"""


class Suspect:
    """Represents a murder suspect."""
    
    def __init__(self, name, motive, alibi, guilty=False):
        """Initialize a suspect.
        
        Args:
            name: Suspect's name
            motive: Why they might have done it
            alibi: Their alibi (can be false)
            guilty: Whether they're actually guilty
        """
        self.name = name
        self.motive = motive
        self.alibi = alibi
        self.guilty = guilty
        self.questioned = False
        self.alibis_verified = False


class VictimProfile:
    """Information about the murder victim."""
    
    def __init__(self):
        """Initialize victim profile."""
        self.name = "Dr. Roj Nemennuh Sarton"
        self.occupation = "Robotics Specialist"
        self.last_seen = "Commissioner's Office at 14:00"
        self.time_of_death = "between 14:30 and 16:00"
        self.cause_of_death = "Blunt force trauma"
        self.motive_info = "Recently discovering a dangerous robot conspiracy"
        self.significance = "His research threatened the balance between humans and robots"


class MysteryPlot:
    """Manages the complete murder mystery."""
    
    def __init__(self):
        """Initialize the mystery plot."""
        self.victim = VictimProfile()
        self.suspects = self._create_suspects()
        self.actual_killer = "Commander Lije Bailey"  # The culprit
        self.murder_motive = "Sarton discovered that certain robots were being secretly modified for dangerous purposes"
        self.revelation_stage = 0  # 0: hidden, 1: partially revealed, 2: fully revealed
    
    def _create_suspects(self):
        """Create all suspects for the case.
        
        Returns:
            dict: Suspects keyed by name
        """
        return {
            "Commissioner": Suspect(
                name="Commissioner",
                motive="Feared Sarton's findings would expose his negligence",
                alibi="Claims he was in his office all afternoon",
                guilty=False
            ),
            "Records Clerk": Suspect(
                name="Records Clerk",
                motive="Recently had a dispute with Sarton about data access",
                alibi="Claims they were processing files in Records",
                guilty=False
            ),
            "Administrator": Suspect(
                name="Administrator",
                motive="Professional rivalry and budget disputes",
                alibi="Verifiable - attended budget meeting until 15:30",
                guilty=False
            ),
            "R. Daneel Olivaw": Suspect(
                name="R. Daneel Olivaw",
                motive="Robots appear suspicious due to victim's robot research",
                alibi="Claim of malfunction during time of death is questionable",
                guilty=False
            ),
        }
    
    def get_suspect_info(self, suspect_name):
        """Get detailed info on a suspect.
        
        Args:
            suspect_name: Name of the suspect
            
        Returns:
            str: Formatted suspect information
        """
        suspect = self.suspects.get(suspect_name)
        if not suspect:
            return "Unknown suspect."
        
        info = f"""
        ┌─ SUSPECT: {suspect.name.upper()} ──────────┐
        │ Motive: {suspect.motive}
        │ Alibi: {suspect.alibi}
        │ Questioned: {'Yes' if suspect.questioned else 'No'}
        │ Alibis Verified: {'Yes' if suspect.alibis_verified else 'No'}
        └─────────────────────────────────────┘
        """
        return info
    
    def verify_alibi(self, suspect_name):
        """Mark a suspect's alibi as verified.
        
        Args:
            suspect_name: Name of the suspect
            
        Returns:
            bool: Whether alibi is solid (rules them out)
        """
        suspect = self.suspects.get(suspect_name)
        if not suspect:
            return False
        
        suspect.alibis_verified = True
        
        # Most alibis are verifiable except for specific ones
        solid_alibis = ["Administrator"]
        return suspect_name in solid_alibis
    
    def question_suspect(self, suspect_name):
        """Mark a suspect as questioned.
        
        Args:
            suspect_name: Name of the suspect
        """
        suspect = self.suspects.get(suspect_name)
        if suspect:
            suspect.questioned = True
    
    def can_accuse(self, player):
        """Check if player has enough evidence to make an accusation.
        
        Args:
            player: Player object
            
        Returns:
            tuple: (can_accuse, required_clues_remaining)
        """
        required_clues = [
            "Victim had critical research on robot conspiracy",
            "Killer had access to crime scene",
            "Forensic evidence matches killer's location",
        ]
        
        found_required = sum(1 for clue in required_clues if clue in player.clues_found)
        can_accuse = found_required >= 2
        
        return can_accuse, len(required_clues) - found_required
    
    def check_solution(self, accused_name):
        """Check if player's accusation is correct.
        
        Args:
            accused_name: Name of the accused person
            
        Returns:
            dict: Solution result with guilty status and explanation
        """
        if accused_name == self.actual_killer:
            return {
                "correct": True,
                "message": f"Your accusation is correct! {accused_name} is the killer!",
                "explanation": self.murder_motive
            }
        else:
            suspect = self.suspects.get(accused_name)
            if suspect:
                return {
                    "correct": False,
                    "message": f"The evidence doesn't support accusing {accused_name}.",
                    "explanation": f"While {accused_name} had motive, the evidence points elsewhere."
                }
            else:
                return {
                    "correct": False,
                    "message": f"You cannot accuse {accused_name}.",
                    "explanation": "That person is not a viable suspect."
                }
    
    def get_mystery_summary(self):
        """Get a summary of the current mystery state.
        
        Returns:
            str: Formatted mystery summary
        """
        summary = f"""
        ╔═════════════════════════════════════════╗
        ║          MURDER INVESTIGATION           ║
        ╠═════════════════════════════════════════╣
        ║ Victim: {self.victim.name}
        ║ Cause: {self.victim.cause_of_death}
        ║ Time: {self.victim.time_of_death}
        ║ Suspects Questioned: {sum(1 for s in self.suspects.values() if s.questioned)}/4
        ║ Alibis Verified: {sum(1 for s in self.suspects.values() if s.alibis_verified)}/4
        ╚═════════════════════════════════════════╝
        """
        return summary
