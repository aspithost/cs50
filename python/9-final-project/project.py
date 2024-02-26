import argparse
import csv
import re
import os
import sys
from tabulate import tabulate


ARGPARSE_MAPPINGS = {
    "name": "full_name",
    "club": "Current Club",
    "goals": "goals_overall",
    "assists": "assists_overall",
    "games": "appearances_overall",
}

NON_FILTER_ARGS = [
    "filename",
    "sort_attribute",
    "sort_order",
    "limit"
]

PLAYER_KEYS = [
    "name",
    "club",
    "games",
    "goals",
    "assists",
    "position",
    "nationality"
]


def main():
    length = len(sys.argv)
    if length == 1:
        sys.exit("Please provide the path to a .csv file with player data. You can also type \"-h\" or \"-help\" for more information.")
    elif length == 2 and sys.argv[1] != "-h" and sys.argv[1] != "--help":
        sys.exit("Use at least 1 command-line argument. "
                 "For more information on how to list "
                 "and filter player data, use \"-h\" or \"-help\".")

    args = parse_arguments()

    # If user did not use a .csv file, return an error
    if os.path.splitext(args.filename)[1] != ".csv":
        sys.exit("Not the correct file type. Please use a .csv file.")

    filters = format_filters(args, NON_FILTER_ARGS)

    players = filter_players(args.filename, filters)
    if not len(players):
        sys.exit("Did not find any matching players! Please try again with different filters.")

    sort_attribute = args.sort_attribute
    sort_order = args.sort_order
    limit = args.limit

    # Sort players
    if sort_attribute:
        players = sort_players(players, sort_attribute, sort_order)

    # Limit number of players returned to user
    players = players[:limit]

    # Format and output players to user
    keys = format_keys(PLAYER_KEYS)

    print(tabulate(format_player_values(players, keys),
                 headers=PLAYER_KEYS,
                 tablefmt="grid"))


# Parses command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A command line tool to "
        "help you filter football player stats!")
    parser.add_argument("filename", type=str,
                        help="A csv file with data of a football season")

    # Groups arguments used for filtering data
    filter_group = parser.add_argument_group(
        "Filters", description="Filter results based on one or more "
        "player attributes. You can even re-use filters with different values!")
    filter_group.add_argument(
        "-n", "--name", type=str, action="append",
        help="The last name of a player")
    filter_group.add_argument(
        "-c", "--club", type=str, action="append",
        help="The name of a club. i.e.: -c \"Manchester City\"")
    filter_group.add_argument(
        "-p", "--position", type=str,
        action="append",
        choices=["goalkeeper", "defender", "midfielder", "forward"],
        help="A player's position")
    filter_group.add_argument(
        "-g", "--goals", type=int, action="append",
        help="The number of goals scored in a season")
    filter_group.add_argument(
        "-a", "--assists", type=int, action="append",
        help="The number of assists in a season")
    filter_group.add_argument(
        "-ga", "--games", type=int, action="append",
        help="The number of games a player has played in a season")
    filter_group.add_argument(
        "-na", "--nationality", type=str, action="append",
        help="The nationality of a player")

    # Groups arguments used for outputting/formatting data.
    format_group = parser.add_argument_group(
        "Formatting options", description="Format the output the way you want; "
        "nobody likes hundreds of lines of players returned arbitrarily!")

    format_group.add_argument(
        "-sa", "--sort-attribute", type=str,
        choices=["name", "club", "position", "goals",
                 "assists", "games", "minutes", "nationality"],
        help="Sort results by a statistic of your choice. "
        "Sort order defaults to descending. Specify --sort-order ascending")
    format_group.add_argument(
        "-so", "--sort-order", type=str, choices=["descending", "ascending"],
        default="descending", help="Sort order when used in combination "
        "with --sort-attribute. Defaults to descending.")
    format_group.add_argument(
        "-lm", "--limit", type=int, action="store",
        help="The number of players returned from searches.")

    return parser.parse_args()


# Formats command-line arguments as dictionary
def format_filters(args, args_to_ignore):
    try:
        return {key: value for key, value in vars(args).items()
                if value and key not in args_to_ignore}
    except TypeError as err:
        print(f"Something went wrong parsing your arguments: {err}")
        raise


# Filteres data from csv file based on user's command-line arguments
def filter_players(filename, filters):
    data = []
    try:
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for player in reader:
                player = filter_player(player, filters)
                if player:
                    data.append(player)
        return data
    except FileNotFoundError:
        print("File does not exist. "
              "Please specify the correct path to a .csv file")
        raise


# Determine if the player matches all the provided filters
def filter_player(player, filters):
    for key, values in filters.items():
        try:
            key_formatted = (
                ARGPARSE_MAPPINGS[key]
                if key in ARGPARSE_MAPPINGS
                else key)
        except KeyError as err:
            print(f"Something went wrong filtering players: {err}")
            raise

        # Determine if a player matches a certain filter
        try:
            if not filter_attribute(player[key_formatted], values):
                return None
        except KeyError as err:
            print(f"Something went wrong filtering players: {err}")
            raise

    # If player matches all filters, return player.
    return player


# Determine if a player's value for an attribute matches
# one of the the user-provided values for said attribute.
def filter_attribute(player_value, values):
    # If user can select multiple values for a fiter
    if isinstance(values, list):
        for value in values:
            if is_matching(player_value, value):
                return True
        return False


# Determine if two values match
def is_matching(player_value, value):
    # For integers, convert to string value to compare with csv string values.
    if isinstance(value, int):
        try:
            return player_value == str(value)
        except TypeError:
            print("Value is not supported, please try again.")
            raise
    # For string values, return partial results
    if isinstance(value, str):
        try:
            return (re.search(value.strip(), player_value, re.IGNORECASE)
                    is not None)
        except (TypeError, AttributeError, re.error) as err:
            print(f"Something went wrong looking for matching players: {err}")
            raise
    raise TypeError("Value is not supported, please try again.")


# Converts string versions of numbers to integers for sorting purposes
def format_player_value(player, sort_attribute):
    player_attribute = (
        ARGPARSE_MAPPINGS[sort_attribute]
        if sort_attribute in ARGPARSE_MAPPINGS
        else sort_attribute) 
    value = player[player_attribute]
    try:
        return (
            int(value)
            if sort_attribute in ["goals", "assists", "games"]
            else value)
    except KeyError as err:
        print(f"KeyError occured: {err}")
        raise err


# Sort players
def sort_players(players, sort_attribute, sort_order):
    try:
        players.sort(key=lambda player:
                     format_player_value(player, sort_attribute),
                     reverse=sort_order == "descending")
        return players
    except (AttributeError, KeyError) as err:
        print(f"An error occured while trying to sort players: {err}")
        raise err


def format_keys(player_keys):
    return [
        ARGPARSE_MAPPINGS[item] if item in ARGPARSE_MAPPINGS
        else item for item in player_keys]


def format_player_values(players, keys):
    try:
        return [
            [player[key] for key in keys] for player in players]
    except KeyError as err:
        print(f"KeyError occured: {err}")
        raise err


if __name__ == "__main__":
    main()

