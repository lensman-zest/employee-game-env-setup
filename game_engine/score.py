"""
Handles individual player scores.
"""

# score.py

def calculate_score(avg_time):
    if avg_time <= 0:
        return 0

    # Score is inversely proportional to average time, scaled for readability
    score = max(1000 - int(avg_time * 1000), 0)
    return score

