"""
Handles leaderboard tracking.
"""

# game_engine/leaderboard.py

leaderboard = []

def update_leaderboard(name, avg_time, score):
    leaderboard.append({
        'name': name,
        'avg_time': avg_time,
        'score': score
    })

def display_leaderboard():
    sorted_leaderboard = sorted(leaderboard, key=lambda x: (-x['score'], x['avg_time']))
    print("\n===== Leaderboard =====")
    for idx, entry in enumerate(sorted_leaderboard, start=1):
        print(f"{idx}. {entry['name']} - Score: {entry['score']} - Avg Time: {entry['avg_time']:.2f}s")
