"""
Handles leaderboard tracking.
"""

# game_engine/leaderboard.py

"""leaderboard = []

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
        print(f"{idx}. {entry['name']} - Score: {entry['score']} - Avg Time: {entry['avg_time']:.2f}s")    """




# leaderboard.py

import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):  # ✅ Make sure it's a dictionary
                    return data
                else:
                    return {}  # Fix corrupted or wrong structure
            except json.JSONDecodeError:
                return {}
    return {}

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)

def update_leaderboard(player_name, new_score, new_time, new_total_rounds):
    leaderboard = load_leaderboard()

    if player_name in leaderboard:
        leaderboard[player_name]["score"] += new_score
        leaderboard[player_name]["total_time"] += new_time
        leaderboard[player_name]["total_rounds"] = new_total_rounds
    else:
        leaderboard[player_name] = {
            "score": new_score,
            "total_time": new_time,
            "total_rounds": new_total_rounds
        }

    save_leaderboard(leaderboard)

def display_leaderboard():
    leaderboard = load_leaderboard()

    if not leaderboard:
        print("🚫 Leaderboard is empty.")
        return

    print("\n🏆 Leaderboard:")
    sorted_leaderboard = sorted(
        leaderboard.items(),
        key=lambda x: (-x[1]["score"], x[1]["total_time"])  # Highest score first, then shortest time
    )

    for rank, (name, data) in enumerate(sorted_leaderboard, start=1):
        print(f"{rank}. {name} - Score: {data['score']}, Total Time: {data['total_time']:.2f} sec, Total Rounds: {data['total_rounds']}")

