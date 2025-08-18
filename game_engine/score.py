"""
Handles score tracking for games.
"""

class ScoreTracker:
    def __init__(self):
        self.score = 0

    def add_points(self, points: int):
        self.score += points

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score
