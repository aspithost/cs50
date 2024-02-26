from random import randint
from sys import exit

def main():
    level = prompt_user("Level")
    random_number = randint(1, level)
    while True:
        guess = prompt_user("Guess")
        if guess < random_number:
            print("Too small!")
        elif guess > random_number:
            print("Too large!")
        else:
            exit("Just right!")


def prompt_user(prompt):
    while True:
        try:
            num = int(input(f"{prompt}: "))
        except ValueError:
            pass
        else:
            if num > 0:
                return num


main()