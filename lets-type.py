import requests
import random
import time
from colorama import Fore, Style


def get_fresh_quote():
    result = ''
    for _ in range(2):
        quotable_api_url = "https://api.quotable.io/random" # Don't Abuse the apis :)
        response = requests.get(quotable_api_url)
        if response.status_code == 200:
            data = response.json()
            quote = data["content"]
            result+= quote + ' '
        else:
            raise Exception(
                "Could not fetch your typing data !! Sorry for the inconvenience"
            )
    return result[:len(result)-1]

def calculate_typing_speed(prompt, start_time, end_time):
    words = len(prompt.split())
    elapsed_time = end_time - start_time
    speed = words / (elapsed_time / 60)
    return speed

def reset_color():
    print(Style.RESET_ALL)

def play_typing_game():
    prompt = get_fresh_quote()
    print( "Type this: ",Fore.GREEN +prompt, "")
    reset_color()
    input("Press ENTER when you are ready!")
    start_time = time.time()
    user_input = input()
    end_time = time.time()
    if user_input == prompt:
        print(Fore.GREEN + "Congratulations! You typed it correctly.")
        reset_color()
    else:
        print(Fore.RED + "Sorry, there were errors in your typing:")
        for i in range(len(prompt)):
            if user_input[i : i + 1] == prompt[i : i + 1]:
                print(Fore.GREEN + user_input[i : i + 1], end="")
            else:
                print(Fore.RED + user_input[i : i + 1], end="")
        reset_color()

    typing_speed = calculate_typing_speed(prompt, start_time, end_time)
    print("Your typing speed: {:.2f} words/minute".format(typing_speed))


if __name__ == "__main__":
    while True:
        play_typing_game()
        play_again = input("Play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break
