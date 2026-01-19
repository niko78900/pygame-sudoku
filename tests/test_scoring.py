import unittest

from scoring import ScoreTracker


class TestScoreTracker(unittest.TestCase):
    def test_valid_scoring_tiers(self):
        tracker = ScoreTracker()
        for index in range(31):
            row = index // 9
            col = index % 9
            delta, scored = tracker.record_valid_move(row, col, 1)
            self.assertTrue(scored)
            self.assertGreater(delta, 0)

        self.assertEqual(tracker.placement_count, 31)
        self.assertEqual(tracker.score, 115)

    def test_invalid_scoring_tiers(self):
        tracker = ScoreTracker()
        for _ in range(10):
            delta = tracker.record_invalid_move()
            self.assertEqual(delta, -1)
        delta = tracker.record_invalid_move()
        self.assertEqual(delta, -2)
        self.assertEqual(tracker.placement_count, 11)
        self.assertEqual(tracker.score, -12)

    def test_repeat_value_after_clear_no_score(self):
        tracker = ScoreTracker()
        tracker.record_clear(0, 0, 5)
        delta, scored = tracker.record_valid_move(0, 0, 5)
        self.assertFalse(scored)
        self.assertEqual(delta, 0)
        self.assertEqual(tracker.score, 0)
        self.assertEqual(tracker.placement_count, 0)

        delta, scored = tracker.record_valid_move(0, 0, 6)
        self.assertTrue(scored)
        self.assertEqual(delta, 2)
        self.assertEqual(tracker.score, 2)
        self.assertEqual(tracker.placement_count, 1)

    def test_completion_bonus(self):
        tracker = ScoreTracker()
        bonus = tracker.apply_completion_bonus()
        self.assertEqual(bonus, 50)
        self.assertEqual(tracker.score, 50)

        tracker.mark_solver_solved()
        bonus = tracker.apply_completion_bonus()
        self.assertEqual(bonus, 0)
        self.assertEqual(tracker.score, 50)


if __name__ == "__main__":
    unittest.main()
