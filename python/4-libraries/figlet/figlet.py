from pyfiglet import Figlet
import sys
from random import randint
from cs50 import get_string

figlet = Figlet()

def main():
    initialize_figlet()
    prompt_user()

#test
#test
__hallo__

def initialize_figlet():
    if (len(sys.argv) != 1 and len(sys.argv) != 3):
        print("Invalid usage")
        sys.exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[1] != "-f" and sys.argv[1] != "--font":
            print("Invalid usage")
            sys.exit(1)
        elif sys.argv[2] not in figlet.getFonts():
            print("Invalid usage")
            sys.exit(1)
        else:
            font = figlet.setFont(font=sys.argv[2])
    else:
        font = figlet.getFonts()[randint(0, 425)]
        figlet.setFont(font=font)


def prompt_user():
    userinput = get_string("Input: ")
    print(figlet.renderText(userinput))


main()
