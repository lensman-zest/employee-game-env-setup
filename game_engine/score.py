"""
Handles individual player scores.
"""

def calculate_score(avg_time):
    if avg_time <= 2:
        return 100
    elif avg_time <= 4:
        return 90
    elif avg_time <= 6:
        return 80
    elif avg_time <= 8:
        return 70
    elif avg_time <= 10:
        return 60
    else:
        return 50
