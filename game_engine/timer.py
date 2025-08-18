"""
Handles game timer logic.
"""

import time

class GameTimer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0

    def get_elapsed_time(self):
        if self.start_time:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time
