import unittest
from game_engine.leaderboard import Leaderboard

class TestLeaderboard(unittest.TestCase):
    def test_add_and_get_top_scores(self):
        lb = Leaderboard()
        lb.add_score("Alice", 100)
        lb.add_score("Bob", 200)
        self.assertEqual(lb.get_top_scores()[0], ("Bob", 200))

    def test_reset_leaderboard(self):
        lb = Leaderboard()
        lb.add_score("Alice", 100)
        lb.reset()
        self.assertEqual(lb.get_top_scores(), [])
 
