import unittest
import time
from game_engine.timer import GameTimer

class TestGameTimer(unittest.TestCase):
    def test_timer_starts_and_gets_elapsed_time(self):
        timer = GameTimer()
        timer.start()
        time.sleep(1)
        self.assertGreater(timer.get_elapsed_time(), 0.9)

    def test_timer_reset(self):
        timer = GameTimer()
        timer.start()
        timer.reset()
        self.assertEqual(timer.get_elapsed_time(), 0)
 
