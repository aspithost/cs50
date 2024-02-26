import sys
import requests
from json import dumps


def main():
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")
    number = get_number()
    data = get_data()
    usd_rate = data["bpi"]["USD"]["rate_float"]
    print(f"${usd_rate * number:,.4f}")


def get_number():
    try:
        return float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")


def get_data():
    try:
        return requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
    except requests.RequestException:
        sys.exit("Something went wrong retrieving your data")



main()