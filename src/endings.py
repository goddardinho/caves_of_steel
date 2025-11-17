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

        # Perfect Justice Ending - Solve with all evidence
        self.endings.append(
            Ending(
                "perfect_justice",
                "THE PERFECT INVESTIGATOR",
                """You correctly identified Julius Enderby as the killer, backed by comprehensive evidence:
the broken eyeglasses, R. Sammy's weapon transport, and the Medievalist conspiracy.

Your detective work was flawless. Enderby is convicted for murder.

R. Daneel reflects: "Your deductive reasoning was exemplary, Detective. 
You have upheld human justice admirably. Sarton did not die in vain."

With this case solved, your reputation in the Caves of Steel is cemented as 
one of the greatest detectives ever. The Commissioner offers you any assignment.

But privately, the Spacers remain unsatisfied. Enderby was supposed to serve 
their cause. Instead, he faces prison. They depart Earth, their mission incomplete.

You have truly solved The Caves of Steel—but at the cost of galactic expansion.""",
                lambda p, gs, mp: (
                    mp.check_solution("Julius Enderby")["correct"]
                    and sum(1 for v in mp.key_evidence.values() if v) >= 4
                ),
                score_bonus=500,
            )
        )

        # Spacer Conspiracy Resolution - Enderby freed to work for Spacers
        self.endings.append(
            Ending(
                "spacer_resolution",
                "THE GREATER GOOD",
                """You identified Julius Enderby as the killer—but the Spacers already knew.

Han Fastolfe approaches you privately: "Detective, Enderby's death was intended 
as R. Daneel's death. A tragic accident. We accept this sacrifice."

He explains the larger picture: Earth's humanity is stagnant. Population declining. 
Technology stagnating. The Spacers had a plan—introduce humanoid robots gradually, 
overcome human prejudice, inspire galactic colonization.

Enderby, they explain, was part of their solution, not their problem. 
His anti-robot faction (the Medievalists) represented a necessary resistance 
to overcome—and a converted Medievalist could influence thousands.

"Commissioner Enderby," Fastolfe continues, "will work with us to promote 
colonization among his former faction. The case will remain officially unsolved. 
Sarton's death becomes the catalyst for change."

You realize you've been used—but perhaps for humanity's greater good.
The Spacers board their ship. Enderby receives a quiet promotion.
Earth enters a new era of human-robot cooperation.

Your conscience remains troubled. Justice compromised for progress.""",
                lambda p, gs, mp: (
                    mp.check_solution("Julius Enderby")["correct"]
                    and sum(1 for v in mp.key_evidence.values() if v) >= 2
                    and sum(1 for v in mp.key_evidence.values() if v) < 4
                ),
                score_bonus=300,
            )
        )

        # Incomplete Investigation - Wrong Suspect
        self.endings.append(
            Ending(
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
                lambda p, gs, mp: (
                    mp.check_solution(mp.actual_killer)["correct"]
                    and p.investigation_points >= 50
                ),
                score_bonus=300,
            )
        )

        # Imperfect Victory Ending
        self.endings.append(
            Ending(
                "imperfect_victory",
                "IMPERFECT JUSTICE",
                """You named someone as the killer, and the evidence seems sufficient. 
However, your investigation was incomplete and hasty.

The suspect is convicted, but you're left with nagging doubts. 
Did you get the right person? Evidence suggests maybe, but it's not certain.

Years later, you still wonder if true justice was served, or if you simply 
condemned the most likely suspect. The case remains a blemish on your record.

The case is closed... but at what cost?""",
                lambda p, gs, mp: (
                    mp.check_solution(mp.actual_killer)["correct"]
                    and p.investigation_points < 50
                ),
                score_bonus=150,
            )
        )

        # Wrongful Conviction Ending
        self.endings.append(
            Ending(
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
                score_bonus=0,
            )
        )

        # Gave Up Ending
        self.endings.append(
            Ending(
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
                lambda p, gs, mp: (
                    gs.time_period == "night"
                    and gs.day >= 3
                    and p.investigation_points < 30
                ),
                score_bonus=50,
            )
        )

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

        # Personalize any references to 'Detective' in the ending text
        try:
            pname = player.name
        except Exception:
            pname = "Detective"

        ending_text = ending.description.replace("Detective", pname).replace(
            "detective", pname
        )

        display = f"""
        ╔═══════════════════════════════════════════════════════════╗
        ║                     GAME OVER                             ║
        ╠═══════════════════════════════════════════════════════════╣
        ║                                                           ║
        ║               {ending.title:^50}        ║
        ║                                                           ║
        ╠═══════════════════════════════════════════════════════════╣
        
        {ending_text}
        
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
