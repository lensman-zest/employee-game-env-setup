import time
import random
import os

LEADERBOARD_FILE = "leaderboard_math_dash.txt"

def generate_question():
    operations = ['+', '-', '*']
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    op = random.choice(operations)
    question = f"{num1} {op} {num2}"
    answer = eval(question)
    return question, answer

def load_leaderboard():
    leaderboard = []
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as file:
            for line in file:
                name, score, avg_time = line.strip().split(',')
                leaderboard.append((name, int(score), float(avg_time)))
    return leaderboard

def save_leaderboard(leaderboard):
    leaderboard.sort(key=lambda x: (-x[1], x[2]))  # Higher score, lower time
    with open(LEADERBOARD_FILE, 'w') as file:
        for name, score, avg_time in leaderboard[:10]:  # Top 10
            file.write(f"{name},{score},{avg_time:.3f}\n")

def display_leaderboard():
    print("\n📊 Leaderboard (Top 10):")
    leaderboard = load_leaderboard()
    if not leaderboard:
        print("No scores yet. Be the first!")
    else:
        for i, (name, score, avg_time) in enumerate(leaderboard, 1):
            print(f"{i}. {name} - 🏆 Score: {score} | ⏱️ Avg Time: {avg_time:.3f}s")

def play_game():
    print("🧠 Welcome to Math Dash Challenge!")
    name = input("Enter your name: ").strip()
    rounds = int(input("How many rounds do you want to play? "))

    score = 0
    times = []

    for r in range(1, rounds + 1):
        print(f"\nRound {r}: Get ready...")
        time.sleep(random.uniform(1.5, 3))

        question, correct_answer = generate_question()
        print(f"❓ Solve: {question}")
        start = time.time()
        try:
            user_answer = int(input("Your answer: "))
            elapsed = time.time() - start
        except ValueError:
            print("Invalid input! No points.")
            times.append(5.0)
            continue

        times.append(elapsed)

        if user_answer == correct_answer:
            print(f"✅ Correct! Time: {elapsed:.3f} seconds")
            points = max(0, 10 - int(elapsed))  # Faster = more points
            score += points
        else:
            print(f"❌ Wrong! Correct was {correct_answer}")
            score -= 2

    avg_time = sum(times) / len(times)
    best_time = min(times)
    worst_time = max(times)

    print(f"\n{name}, your total score: {score}")
    print(f"⏱️ Average time: {avg_time:.3f} seconds")
    print(f"⚡ Fastest time: {best_time:.3f} seconds")
    print(f"🐢 Slowest time: {worst_time:.3f} seconds")

    leaderboard = load_leaderboard()
    leaderboard.append((name, score, avg_time))
    save_leaderboard(leaderboard)
    display_leaderboard()

    print("🎉 Thanks for playing Math Dash Challenge!")

if __name__ == "__main__":
    play_game()
