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


class Faction:
    """Represents a political faction in the game world."""

    def __init__(self, name, ideology, goal, methods):
        """Initialize a faction.

        Args:
            name: Faction name
            ideology: Their core beliefs
            goal: What they're trying to achieve
            methods: How they operate
        """
        self.name = name
        self.ideology = ideology
        self.goal = goal
        self.methods = methods


class VictimProfile:
    """Information about the murder victim."""

    def __init__(self):
        """Initialize victim profile."""
        self.name = "Dr. Roj Nemennuh Sarton"
        self.occupation = "Robotics Specialist (Spacer)"
        self.last_seen = "Spacetown at 14:30"
        self.time_of_death = "between 14:45 and 16:00"
        self.cause_of_death = "Blaster wound (mistaken identity)"
        self.motive_info = "Intended victim was R. Daneel Olivaw; Sarton's designer/creator"
        self.significance = (
            "His death was intended to be the target assassin was aiming at R. Daneel. "
            "The true target was not Sarton but the humanoid robot he created."
        )


class MysteryPlot:
    """Manages the complete murder mystery."""

    def __init__(self):
        """Initialize the mystery plot."""
        self.victim = VictimProfile()
        self.suspects = self._create_suspects()
        self.factions = self._create_factions()
        self.actual_killer = "Julius Enderby"  # The actual murderer
        self.murder_motive = (
            "Enderby, secretly a Medievalist, wanted to destroy R. Daneel. "
            "He ordered R. Sammy to transport a blaster through the country. "
            "His broken glasses caused him to kill Sarton instead of R. Daneel."
        )
        self.revelation_stage = 0  # 0: hidden, 1: partially revealed, 2: fully revealed
        self.key_evidence = {
            "eyeglass_fragments": False,
            "r_sammy_transport": False,
            "enderby_medievalist": False,
            "spacer_conspiracy": False,
            "broken_glasses_found": False,
        }
        self.time_remaining = 90  # Minutes until Spacers leave Earth
        self.case_breakthrough = False

    def _create_factions(self):
        """Create all political factions.

        Returns:
            dict: Factions keyed by name
        """
        return {
            "Spacer_Expansionists": Faction(
                name="Spacer Expansionists",
                ideology="Spacer culture is stagnating; Earth colonization is necessary",
                goal="Introduce humanoid robots to Earth to overcome human prejudice",
                methods="Diplomatic, suggestive drugs, subtle cultural introduction",
            ),
            "Medievalists": Faction(
                name="Medievalists",
                ideology="Humanity should return to pre-cave society; robots are unnatural",
                goal="Destroy robot presence on Earth; eliminate human-robot cooperation",
                methods="Sabotage, assassination, subversion from within",
            ),
            "Earth_Officials": Faction(
                name="Earth Officials",
                ideology="Maintain order in the caves of steel",
                goal="Protect Earth citizens and maintain political stability",
                methods="Investigation, law enforcement, bureaucracy",
            ),
        }

    def _create_suspects(self):
        """Create all suspects for the case.

        Returns:
            dict: Suspects keyed by name
        """
        return {
            "Julius Enderby": Suspect(
                name="Julius Enderby",
                motive="Secret Medievalist; intended to kill R. Daneel Olivaw to strike against robot presence",
                alibi="Claims he was in his office all afternoon (FALSE — he was in Spacetown)",
                guilty=True,  # THE ACTUAL KILLER
            ),
            "Records Clerk": Suspect(
                name="Records Clerk",
                motive="Had a data access dispute with Sarton",
                alibi="Verifiable — was processing files with witnesses",
                guilty=False,
            ),
            "Administrator": Suspect(
                name="Administrator",
                motive="Professional rivalry over robotics research funding",
                alibi="Verifiable — attended budget meeting until 15:30",
                guilty=False,
            ),
            "R. Daneel Olivaw": Suspect(
                name="R. Daneel Olivaw",
                motive="Robots appear suspicious due to victim's robot research",
                alibi="Provably with Baley during time of death",
                guilty=False,
            ),
            "Francis Clousarr": Suspect(
                name="Francis Clousarr",
                motive="Anti-robot activist; believed Sarton was dangerous",
                alibi="No verifiable alibi, but wrong means/method",
                guilty=False,
            ),
            "Han Fastolfe": Suspect(
                name="Han Fastolfe",
                motive="Professional conflict with Sarton over research approach",
                alibi="At Spacer Embassy with limited staff",
                guilty=False,
            ),
            "R. Sammy": Suspect(
                name="R. Sammy",
                motive="Following Enderby's orders (no independent motive)",
                alibi="Transported weapon but did not commit murder",
                guilty=False,  # Accomplice, but bound by First Law
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

        # Strong alibis rule out suspects
        solid_alibis = ["Administrator", "Records Clerk", "R. Daneel Olivaw"]
        return suspect_name in solid_alibis

    def question_suspect(self, suspect_name):
        """Mark a suspect as questioned.

        Args:
            suspect_name: Name of the suspect
        """
        suspect = self.suspects.get(suspect_name)
        if suspect:
            suspect.questioned = True

    def record_evidence(self, evidence_name):
        """Record discovery of key evidence.

        Args:
            evidence_name: Key from evidence dict
        """
        if evidence_name in self.key_evidence:
            self.key_evidence[evidence_name] = True

    def can_accuse(self, player):
        """Check if player has enough evidence to make an accusation.

        Args:
            player: Player object

        Returns:
            tuple: (can_accuse, required_clues_remaining)
        """
        # Need at least 3 evidence points to accuse
        evidence_found = sum(1 for v in self.key_evidence.values() if v)
        can_accuse = evidence_found >= 3

        return can_accuse, max(0, 3 - evidence_found)

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
                "message": f"Your accusation is CORRECT! {accused_name} is the killer!",
                "explanation": self.murder_motive,
                "case_solved": True,
            }
        else:
            suspect = self.suspects.get(accused_name)
            if suspect:
                if suspect.guilty:
                    return {
                        "correct": False,
                        "message": f"Close, but {accused_name} is not the primary killer.",
                        "explanation": f"{accused_name} was involved but not the main perpetrator.",
                        "case_solved": False,
                    }
                else:
                    return {
                        "correct": False,
                        "message": f"The evidence doesn't support accusing {accused_name}.",
                        "explanation": f"While {accused_name} had motive/opportunity, the real evidence points elsewhere.",
                        "case_solved": False,
                    }
            else:
                return {
                    "correct": False,
                    "message": f"You cannot accuse {accused_name}.",
                    "explanation": "That person is not a viable suspect in this investigation.",
                    "case_solved": False,
                }

    def get_mystery_summary(self):
        """Get a summary of the current mystery state.

        Returns:
            str: Formatted mystery summary
        """
        evidence_count = sum(1 for v in self.key_evidence.values() if v)
        summary = f"""
        ╔═════════════════════════════════════════╗
        ║          MURDER INVESTIGATION           ║
        ╠═════════════════════════════════════════╣
        ║ Victim: {self.victim.name}
        ║ Cause: {self.victim.cause_of_death}
        ║ Time: {self.victim.time_of_death}
        ║ Suspects Questioned: {sum(1 for s in self.suspects.values() if s.questioned)}/7
        ║ Alibis Verified: {sum(1 for s in self.suspects.values() if s.alibis_verified)}/7
        ║ Evidence Found: {evidence_count}/5
        ║ Time Until Spacers Leave: {self.time_remaining} min
        ╚═════════════════════════════════════════╝
        """
        return summary
