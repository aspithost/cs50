import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")
    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# TODO: Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    new_cases = {}
    previous_cases = {}
    for row in reader:
        state = row["state"]
        cases = row["cases"]

        if state not in new_cases:
            new_cases[state] = [int(cases)]
            previous_cases[state] = [int(cases)]

        else:
            length = len(new_cases[state])
            new_cases[state] += [int(int(cases) - previous_cases[state][length - 1])]
            previous_cases[state] += [int(cases)]

            if length > 13:
                new_cases[state].pop(0)
                previous_cases[state].pop(0)
    return new_cases

# TODO: Calculate and print out seven day average for given state
def comparative_averages(new_cases, states):
    for state in states:
        old_average = 0
        new_average = 0
        for cases in new_cases[state][0:7]:
            old_average += cases
        for cases in new_cases[state][7:]:
            new_average += cases

        try:
        # print(new_average, old_average)
            average = round((new_average - old_average) / old_average * 100)
            new_average = new_average / 7

            print(f"{state} had a 7-day average of {round(new_average)} and an {f'increase of {average}%' if average > 0 else f'decrease of {average}%'} " )
        # print(f"{state} had a 7-day average of {new_average}" )
        except ZeroDivisionError:
            print(f"{state} had a 7-day average of {round(new_average / 7)} with an increase of 0%")


main()
