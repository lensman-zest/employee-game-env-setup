import time
import random
import os

LEADERBOARD_FILE = "leaderboard.txt"

def get_score(reaction_time):
    if reaction_time < 0.3:
        return 100
    elif reaction_time <= 0.6:
        return 50
    else:
        return 10

def save_to_leaderboard(name, average_time, score):
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{name},{average_time:.3f},{score}\n")

def display_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        print("\n🏆 Leaderboard is empty!")
        return
    
    print("\n🏆 Leaderboard:")
    with open(LEADERBOARD_FILE, "r") as file:
        records = [line.strip().split(",") for line in file.readlines()]
    
    # Sort by score descending, then avg time ascending
    records.sort(key=lambda x: (-int(x[2]), float(x[1])))
    
    print(f"{'Rank':<5}{'Name':<15}{'Avg Time (s)':<15}{'Score':<10}")
    print("-" * 45)
    for i, (name, avg_time, score) in enumerate(records[:10], 1):
        print(f"{i:<5}{name:<15}{avg_time:<15}{score:<10}")

def main():
    print("🎮 Welcome to QuickTap Challenge!")
    name = input("Enter your name: ").strip()
    rounds = int(input("How many rounds do you want to play? "))
    
    reaction_times = []
    total_score = 0
    
    for round_num in range(1, rounds + 1):
        print(f"\nRound {round_num}: Get ready...")
        time.sleep(random.randint(2, 5))
        print("🔔 Press ENTER now!")
        input()
        start = time.perf_counter()
        input("✅ Quick! Press ENTER again!\n")
        end = time.perf_counter()
        
        reaction_time = end - start
        reaction_times.append(reaction_time)
        score = get_score(reaction_time)
        total_score += score
        
        print(f"⏱️ Reaction time: {reaction_time:.3f} seconds")
        print(f"🎯 Score this round: {score}")
    
    average_time = sum(reaction_times) / rounds
    best_time = min(reaction_times)
    worst_time = max(reaction_times)
    
    print(f"\n{name}, your average reaction time: {average_time:.3f} seconds")
    print(f"⚡ Best time: {best_time:.3f} seconds")
    print(f"🐢 Slowest time: {worst_time:.3f} seconds")
    print(f"🏅 Total Score: {total_score}")
    
    save_to_leaderboard(name, average_time, total_score)
    display_leaderboard()
    print("🎉 Thanks for playing QuickTap Challenge!")

if __name__ == "__main__":
    main()
