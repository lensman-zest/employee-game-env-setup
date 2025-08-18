import unittest
from game_engine.score import ScoreTracker

class TestScoreTracker(unittest.TestCase):
    def test_add_points(self):
        st = ScoreTracker()
        st.add_points(10)
        self.assertEqual(st.get_score(), 10)

    def test_reset_score(self):
        st = ScoreTracker()
        st.add_points(15)
        st.reset_score()
        self.assertEqual(st.get_score(), 0)

# ✅ Required to run the tests when using `python tests/test_score.py`
if __name__ == "__main__":
    unittest.main()
