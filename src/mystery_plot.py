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
        self.cause_of_death = "Blaster wound"
        self.motive_info = "Victim of a conspiracy involving Earth and Spacer factions"
        self.significance = (
            "His death marks a critical turning point in human-robot relations on Earth. "
            "Political powers vie to control the investigation's outcome."
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
        # Map evidence to suspects
        self.evidence_links = {
            "eyeglass_fragments": ["Julius Enderby"],
            "r_sammy_transport": ["R. Sammy", "Julius Enderby"],
            "enderby_medievalist": ["Julius Enderby"],
            "spacer_conspiracy": ["Han Fastolfe"],
            "broken_glasses_found": ["Julius Enderby"],
        }
        self.time_remaining = 1440  # Minutes until Spacers leave Earth (24 hours, canon-accurate)
        self.case_breakthrough = False
        self.history = []  # Investigation action log
        self.locked_suspects = set()  # Suspects locked by choices
        self.locked_evidence = set()  # Evidence locked by choices

    def advance_time(self, minutes):
        """Advance time and check for expiration."""
        self.time_remaining = max(0, self.time_remaining - minutes)
        self.history.append(f"Time advanced by {minutes} min. Remaining: {self.time_remaining} min.")
        if self.time_remaining == 0:
            self.history.append("Time expired! Investigation forced to end.")
            # Could trigger a forced ending here

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
                alibi="At Spacetown with limited staff",
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
        if suspect_name in self.locked_suspects:
            self.history.append(f"Cannot verify alibi for {suspect_name}: suspect is locked.")
            return False
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
        self.history.append(f"Alibi verified for {suspect_name}.")

        # Strong alibis rule out suspects
        solid_alibis = ["Administrator", "Records Clerk", "R. Daneel Olivaw"]
        return suspect_name in solid_alibis

    def question_suspect(self, suspect_name):
        if suspect_name in self.locked_suspects:
            self.history.append(f"Cannot question {suspect_name}: suspect is locked.")
            return
        """Mark a suspect as questioned.

        Args:
            suspect_name: Name of the suspect
        """
        suspect = self.suspects.get(suspect_name)
        if suspect:
            suspect.questioned = True
            self.history.append(f"Questioned {suspect_name}.")

    def record_evidence(self, evidence_name):
        if evidence_name in self.locked_evidence:
            self.history.append(f"Cannot record evidence {evidence_name}: evidence is locked.")
            return
        """Record discovery of key evidence.

        Args:
            evidence_name: Key from evidence dict
        """
        if evidence_name in self.key_evidence:
            self.key_evidence[evidence_name] = True
            linked = self.evidence_links.get(evidence_name, [])
            self.history.append(f"Found evidence: {evidence_name} (implicates: {', '.join(linked) if linked else 'unknown'})")

    def branch_choice(self, choice):
        """Branch investigation based on player choice."""
        # Example: lock/unlock suspects/evidence based on choice
        if choice == "trust_spacers":
            self.locked_suspects.add("Francis Clousarr")
            self.locked_evidence.add("spacer_conspiracy")
            self.history.append("Branch: Trusted Spacers. Clousarr and spacer_conspiracy locked.")
        elif choice == "pursue_medievalists":
            self.locked_suspects.add("Han Fastolfe")
            self.locked_evidence.add("r_sammy_transport")
            self.history.append("Branch: Pursued Medievalists. Fastolfe and r_sammy_transport locked.")

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
        ruled_out = [s.name for s in self.suspects.values() if s.alibis_verified and not s.guilty]
        timeline = '\n'.join(self.history[-5:]) if self.history else 'No actions yet.'
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
        ║ Ruled Out: {', '.join(ruled_out) if ruled_out else 'None'}
        ║ Locked Suspects: {', '.join(self.locked_suspects) if self.locked_suspects else 'None'}
        ║ Locked Evidence: {', '.join(self.locked_evidence) if self.locked_evidence else 'None'}
        ║ Recent Actions: 
        ║   {timeline}
        ╚═════════════════════════════════════════╝
        """
        return summary
