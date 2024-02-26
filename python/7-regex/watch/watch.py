import re
import sys


def main():
    print(parse(input("HTML: ").strip()))


def parse(s):
    if matches := re.search(r"<iframe.+src=\"https?:\/\/(www\.)?youtube\.com\/embed\/(\w+)\".*<\/iframe>", s, re.IGNORECASE):
        return f"https://youtu.be/{matches.group(2)}"


if __name__ == "__main__":
    main()