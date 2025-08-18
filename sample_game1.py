from game_engine.timer import start_timer, stop_timer, get_time_difference
from game_engine.score import calculate_score
from game_engine.leaderboard import update_leaderboard, display_leaderboard

def play_game():
    name = input("Enter your name: ")
    rounds = int(input(f"Hi {name}, how many rounds would you like to play? "))

    total_time = 0
    for round_num in range(1, rounds + 1):
        input(f"\nRound {round_num}: Press Enter to start...")
        start = start_timer()

        input("Press Enter to stop...")
        end = stop_timer()

        round_time = get_time_difference(start, end)
        print(f"Time taken: {round_time}s")
        total_time += round_time

    avg_time = round(total_time / rounds, 2)
    score = calculate_score(avg_time)

    print(f"\nGame over for {name}! Average Time: {avg_time}s | Score: {score}")
    update_leaderboard(name, avg_time, score)

def main():
    while True:
        play_game()
        choice = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if choice != 'yes':
            break

    display_leaderboard()

if __name__ == "__main__":
    main()
