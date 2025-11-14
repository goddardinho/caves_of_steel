"""
Multiple Endings System - Different endings based on player choices
"""


class Ending:
    """Represents a game ending."""
    
    def __init__(self, ending_id, title, description, conditions, score_bonus=0):
        """Initialize an ending.
        
        Args:
            ending_id: Unique ending ID
            title: Ending title
            description: Ending story
            conditions: Function that checks if this ending is reached
            score_bonus: Points awarded for this ending
        """
        self.ending_id = ending_id
        self.title = title
        self.description = description
        self.conditions = conditions
        self.score_bonus = score_bonus


class EndingsManager:
    """Manages game endings."""
    
    def __init__(self):
        """Initialize endings manager."""
        self.endings = []
        self._create_endings()
    
    def _create_endings(self):
        """Create all possible endings."""
        
        # Perfect Justice Ending
        self.endings.append(Ending(
            "perfect_justice",
            "THE PERFECT INVESTIGATOR",
            """You correctly identified the killer and gathered all evidence without errors.
Your detective work was flawless, and the killer is now facing justice.
R. Daneel reflects: "Your deductive reasoning was exemplary, Detective. 
You have upheld human justice admirably."

With this case solved, your reputation in the Caves of Steel is cemented as 
one of the greatest detectives ever. The Commissioner offers you any assignment 
you wish.

You have truly solved The Caves of Steel.""",
            lambda p, gs, mp: (mp.check_solution(mp.actual_killer)["correct"] and 
                             len(p.clues_found) >= 8 and
                             p.investigation_points >= 100),
            score_bonus=500
        ))
        
        # Justice Served Ending
        self.endings.append(Ending(
            "justice_served",
            "JUSTICE SERVED",
            """You identified and convicted the killer. Though your investigation wasn't 
perfect, you gathered enough evidence to prove guilt beyond doubt.

The killer is taken into custody. The Commissioner commends your work: 
"Good job, Detective. This case is closed."

The Caves of Steel can rest easy knowing the murderer is behind bars.
Your partnership with R. Daneel has also proven that humans and robots can 
work together effectively.

The case is closed.""",
            lambda p, gs, mp: (mp.check_solution(mp.actual_killer)["correct"] and 
                             p.investigation_points >= 50),
            score_bonus=300
        ))
        
        # Imperfect Victory Ending
        self.endings.append(Ending(
            "imperfect_victory",
            "IMPERFECT JUSTICE",
            """You named someone as the killer, and the evidence seems sufficient. 
However, your investigation was incomplete and hasty.

The suspect is convicted, but you're left with nagging doubts. 
Did you get the right person? Evidence suggests maybe, but it's not certain.

Years later, you still wonder if true justice was served, or if you simply 
condemned the most likely suspect. The case remains a blemish on your record.

The case is closed... but at what cost?""",
            lambda p, gs, mp: (mp.check_solution(mp.actual_killer)["correct"] and 
                             p.investigation_points < 50),
            score_bonus=150
        ))
        
        # Wrongful Conviction Ending
        self.endings.append(Ending(
            "wrongful_conviction",
            "GRAVE MISTAKE",
            """You accused the wrong person. With your detective badge as proof of your 
authority, an innocent person is convicted.

The real killer remains free in the Caves of Steel, continuing their dangerous 
activities. Later, evidence emerges proving the convicted person's innocence.

You are stripped of your badge and expelled from the force. The Commissioner's 
words haunt you: "You had one job, Detective. You failed."

R. Daneel states, in typical robotic fashion: "Your logical reasoning process 
appeared sound, but the conclusion was incorrect. I suggest introspection."

Your career is over. The real murderer walks free.

THE WORST ENDING.""",
            lambda p, gs, mp: not mp.check_solution(mp.actual_killer)["correct"],
            score_bonus=0
        ))
        
        # Gave Up Ending
        self.endings.append(Ending(
            "gave_up",
            "UNSOLVED MYSTERY",
            """You never gathered enough evidence or clues to make an accusation. 
Time runs out, and the case goes cold.

The killer remains at large. The victim's family never receives closure. 
The incident becomes an unsolved mystery, one of the great failures of 
the Caves of Steel police department.

The Commissioner demotes you: "You had three days, Detective. You had all 
the evidence you needed. What happened?"

You spend the rest of your career on desk duty, wondering about the 
murder that got away.

THE CASE REMAINS UNSOLVED.""",
            lambda p, gs, mp: (gs.time_period == "night" and gs.day >= 3 and 
                             p.investigation_points < 30),
            score_bonus=50
        ))
    
    def check_ending(self, player, game_state, mystery_plot):
        """Check which ending conditions are met.
        
        Args:
            player: Player object
            game_state: GameState object
            mystery_plot: MysteryPlot object
            
        Returns:
            Ending or None
        """
        for ending in sorted(self.endings, key=lambda e: e.score_bonus, reverse=True):
            try:
                if ending.conditions(player, game_state, mystery_plot):
                    return ending
            except Exception:
                continue
        
        return None
    
    def display_ending(self, ending, player):
        """Display an ending to the player.
        
        Args:
            ending: Ending object
            player: Player object
            
        Returns:
            str: Formatted ending
        """
        final_score = player.investigation_points + ending.score_bonus
        
        display = f"""
        ╔═══════════════════════════════════════════════════════════╗
        ║                     GAME OVER                             ║
        ╠═══════════════════════════════════════════════════════════╣
        ║                                                           ║
        ║               {ending.title:^50}        ║
        ║                                                           ║
        ╠═══════════════════════════════════════════════════════════╣
        
        {ending.description}
        
        ╠═══════════════════════════════════════════════════════════╣
        ║                  INVESTIGATION COMPLETE                  ║
        ║ Final Score: {final_score} points
        ║ Clues Found: {len(player.clues_found)}
        ║ Characters Met: {len(player.met_characters)}
        ║ Investigation Points: {player.investigation_points}
        ╚═══════════════════════════════════════════════════════════╝
        """
        return display
    
    def get_ending_stats(self):
        """Get statistics about the endings.
        
        Returns:
            str: Formatted endings info
        """
        stats = "\n📊 POSSIBLE ENDINGS:\n"
        for ending in self.endings:
            stats += f"  • {ending.title} ({ending.score_bonus} pts)\n"
        return stats
