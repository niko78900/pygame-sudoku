from dataclasses import dataclass, field
from typing import Dict, Tuple


def score_delta(placement_count, is_correct):
    if placement_count <= 10:
        return 2 if is_correct else -1
    if placement_count <= 20:
        return 4 if is_correct else -2
    if placement_count <= 30:
        return 5 if is_correct else -3
    return 5 if is_correct else -6


@dataclass
class ScoreTracker:
    score: int = 0
    placement_count: int = 0
    solver_used: bool = False
    last_cleared_values: Dict[Tuple[int, int], int] = field(default_factory=dict)

    def reset(self):
        self.score = 0
        self.placement_count = 0
        self.solver_used = False
        self.last_cleared_values.clear()

    def record_valid_move(self, row, col, value):
        if self.last_cleared_values.get((row, col)) == value:
            return 0, False
        self.placement_count += 1
        delta = score_delta(self.placement_count, True)
        self.score += delta
        return delta, True

    def record_invalid_move(self):
        self.placement_count += 1
        delta = score_delta(self.placement_count, False)
        self.score += delta
        return delta

    def record_clear(self, row, col, previous_value):
        if previous_value != 0:
            self.last_cleared_values[(row, col)] = previous_value

    def mark_solver_solved(self):
        self.solver_used = True

    def apply_completion_bonus(self):
        if self.solver_used:
            return 0
        self.score += 50
        return 50
