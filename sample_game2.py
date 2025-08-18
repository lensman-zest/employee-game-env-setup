# sample_game2.py

import random
from game_engine.timer import start_timer, stop_timer, get_time_difference
from game_engine.score import calculate_score
from game_engine.leaderboard import update_leaderboard, display_leaderboard

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a useful skill for many professions.",
    "Practice makes perfect in everything you do.",
    "Always check your work before submitting it.",
    "Consistency is the key to mastering anything.",
    "Python is a versatile and powerful language.",
    "Fast and accurate typing can save you time.",
    "Errors are part of learning, don't fear them.",
    "Focus on accuracy before increasing speed.",
    "Great developers write clean and readable code.",
    "Time management is crucial in daily life.",
    "Success comes to those who work for it.",
    "Communication is essential in a good team.",
    "Debugging code can be frustrating but rewarding.",
    "Challenges make you stronger and more resilient.",
    "Always be open to learning new things.",
    "Good habits lead to great achievements.",
    "Patience and persistence conquer all problems.",
    "A well-structured program is easy to maintain.",
    "Comments help others understand your code."
]

def main():
    players = int(input("Enter number of players: "))
    rounds = int(input("Enter number of rounds per player: "))

    for _ in range(players):
        name = input("\nEnter your name: ")
        total_time = 0

        for i in range(rounds):
            sentence = random.choice(sentences)
            print(f"\n{name}, round {i + 1}:")
            print(f"Type this sentence:\n{sentence}")
            input("Press Enter to start...")
            start = start_timer()
            typed = input(">> ")
            end = stop_timer()
            elapsed = get_time_difference(start, end)

            if typed.strip() != sentence:
                print("Incorrect typing! Time penalty added.")
                elapsed += 2  # 2-second penalty

            print(f"Round {i + 1} Time: {elapsed:.2f}s")
            total_time += elapsed

        avg_time = total_time / rounds
        score = calculate_score(avg_time)
        print(f"\nGame over for {name}! Average Time: {avg_time:.2f}s | Score: {score}")
        update_leaderboard(name, avg_time, score)

    display_leaderboard()

if __name__ == "__main__":
    main()
