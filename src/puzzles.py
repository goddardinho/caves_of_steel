"""
Puzzle System - Interactive puzzles and challenges
"""


class Puzzle:
    """Base puzzle class."""

    def __init__(self, puzzle_id, description, solution):
        """Initialize puzzle.

        Args:
            puzzle_id: Unique puzzle ID
            description: Puzzle description
            solution: The correct solution/answer
        """
        self.puzzle_id = puzzle_id
        self.description = description
        self.solution = solution.lower().strip()
        self.solved = False
        self.attempts = 0

    def check_solution(self, answer):
        """Check if the answer is correct.

        Args:
            answer: Player's answer

        Returns:
            bool: Whether the answer is correct
        """
        self.attempts += 1
        if answer.lower().strip() == self.solution:
            self.solved = True
            return True
        return False

    def get_hints(self):
        """Get hints for the puzzle.

        Returns:
            list: List of hints
        """
        return ["Think about the clues you've gathered."]


class AccessCodePuzzle(Puzzle):
    """Puzzle to access restricted area - requires finding code."""

    def __init__(self):
        """Initialize access code puzzle."""
        super().__init__(
            "access_code",
            "The Records Office door has a numerical lock. You need to find the correct 4-digit code.",
            "1955",  # Year Asimov wrote "The Caves of Steel"
        )
        self.hints_given = 0

    def get_hints(self):
        """Get hints for the access code."""
        hints = [
            "It's a significant year in science fiction history.",
            "Look at the book publication year and related documents.",
            "Think about when this story was created by the author.",
            "The code is 1-9-5-5. Years with double digits!",
        ]
        if self.hints_given < len(hints):
            hint = hints[self.hints_given]
            self.hints_given += 1
            return hint
        return "You've exhausted the hints. Keep trying!"


class LogicPuzzle(Puzzle):
    """Puzzle requiring deductive reasoning."""

    def __init__(self):
        """Initialize logic puzzle."""
        super().__init__(
            "logic_puzzle",
            "Three suspects: Commissioner, Records Clerk, Administrator. One is lying. Who?",
            "records clerk",
        )

    def get_hints(self):
        """Get hints for the logic puzzle."""
        return [
            "Look for contradictions in their alibis.",
            "The Commissioner's alibi can be verified.",
            "The Administrator was in a documented meeting.",
            "Focus on who had the most opportunity.",
        ]


class SequencePuzzle(Puzzle):
    """Pattern recognition puzzle."""

    def __init__(self):
        """Initialize sequence puzzle."""
        super().__init__(
            "sequence", "Complete the sequence: Steel, Robots, Murder, ?", "justice"
        )

    def get_hints(self):
        """Get hints for the sequence puzzle."""
        return [
            "Think about the themes of the story.",
            "It relates to the investigation's ultimate goal.",
            "What are you trying to achieve as a detective?",
        ]


class PuzzleManager:
    """Manages all puzzles in the game."""

    def __init__(self):
        """Initialize puzzle manager."""
        self.puzzles = {
            "access_code": AccessCodePuzzle(),
            "logic_puzzle": LogicPuzzle(),
            "sequence": SequencePuzzle(),
        }

    def get_puzzle(self, puzzle_id):
        """Get a puzzle by ID.

        Args:
            puzzle_id: Puzzle ID

        Returns:
            Puzzle or None
        """
        return self.puzzles.get(puzzle_id)

    def solve_puzzle(self, puzzle_id, answer):
        """Attempt to solve a puzzle.

        Args:
            puzzle_id: Puzzle ID
            answer: Player's answer

        Returns:
            dict: Result with success status and feedback
        """
        puzzle = self.get_puzzle(puzzle_id)
        if not puzzle:
            return {"success": False, "message": "Puzzle not found."}

        if puzzle.solved:
            return {"success": True, "message": "You've already solved this puzzle!"}

        if puzzle.check_solution(answer):
            return {
                "success": True,
                "message": f"✅ Correct! You've solved the '{puzzle_id}' puzzle!",
                "reward": 50,
            }
        else:
            attempts_text = (
                f" (Attempt {puzzle.attempts})" if puzzle.attempts > 1 else ""
            )
            return {
                "success": False,
                "message": f"❌ Incorrect answer.{attempts_text}",
                "attempts": puzzle.attempts,
            }

    def get_hint(self, puzzle_id):
        """Get a hint for a puzzle.

        Args:
            puzzle_id: Puzzle ID

        Returns:
            str: Hint text
        """
        puzzle = self.get_puzzle(puzzle_id)
        if not puzzle:
            return "Puzzle not found."

        if puzzle.solved:
            return "You've already solved this puzzle."

        hints = puzzle.get_hints()
        if isinstance(hints, list):
            hint_index = min(puzzle.attempts, len(hints) - 1)
            return hints[hint_index]
        return hints

    def get_solved_puzzles(self):
        """Get count of solved puzzles.

        Returns:
            tuple: (solved_count, total_count)
        """
        solved = sum(1 for p in self.puzzles.values() if p.solved)
        total = len(self.puzzles)
        return solved, total
