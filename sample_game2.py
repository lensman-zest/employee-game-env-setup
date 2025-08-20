import random
from game_engine.timer import Timer
from game_engine.score import calculate_score
from game_engine.leaderboard import update_leaderboard, display_leaderboard

def generate_question():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(['+', '-', '*'])

    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2

    question = f"What is {num1} {operation} {num2}? "
    return question, answer

def main():
    player_name = input("Enter your name: ")
    rounds = int(input("Enter number of rounds to play: "))

    total_time = 0

    for i in range(rounds):
        print(f"\nRound {i+1}:")
        question, correct_answer = generate_question()
        print(question)

        timer = Timer()
        timer.start()
        user_answer = input("Your answer: ")
        elapsed = timer.stop()

        try:
            if int(user_answer.strip()) == correct_answer:
                print(f"Correct! Time taken: {elapsed:.2f} seconds.")
            else:
                print(f"Wrong. The correct answer was {correct_answer}. Time taken: {elapsed:.2f} seconds.")
        except ValueError:
            print(f"Invalid input. The correct answer was {correct_answer}. Time taken: {elapsed:.2f} seconds.")

        total_time += elapsed

    average_time = total_time / rounds
    score = calculate_score(average_time)

    print(f"\nGame Over! Total time: {total_time:.2f} seconds | Average time: {average_time:.2f} seconds")
    print(f"Your score: {score:.2f}")

    update_leaderboard(player_name, score, total_time)
    display_leaderboard()

if __name__ == "__main__":
    main()
