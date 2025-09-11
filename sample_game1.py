# sample_game1.py

import time
from game_engine.timer import Timer
from game_engine.score import calculate_score
from game_engine.leaderboard import update_leaderboard, display_leaderboard

def sample_game1(player_name, rounds):
    print(f"\nWelcome, {player_name}! Get ready for Sample Game 1 🎮")
    print("Your goal is to press Enter as fast as you can when prompted.\n")

    total_time = 0

    for i in range(1, rounds + 1):
        input(f"Round {i}: Press Enter to start...")
        print("Wait for it...")
        time.sleep(1)  # short pause to avoid immediate Enter hit
        input("Now! Press Enter as fast as you can!")
        
        timer = Timer()
        timer.start()
        input()  # Wait for the user's quick reaction
        elapsed = timer.stop()

        print(f"⏱ Time taken: {elapsed:.3f} seconds\n")
        total_time += elapsed

    average_time = total_time / rounds
    score = calculate_score(average_time)

    print(f"\n✅ Game Over, {player_name}!")
    print(f"🎯 Total Time: {total_time:.2f} seconds")
    print(f"🎯 Total Rounds: {rounds}")
    print(f"📊 Average Time per Round: {average_time:.2f} seconds")
    print(f"🏅 Score: {score}")

    update_leaderboard(player_name, score, total_time, rounds)
    display_leaderboard()

if __name__ == "__main__":
    name = input("Enter your name: ")
    rounds = int(input("How many rounds do you want to play? "))
    sample_game1(name, rounds)
