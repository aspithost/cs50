import csv
from sys import argv, exit


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        exit("Requires two command line arguments")

    with open(argv[1]) as csv_file:
        # Create list with all people's data
        rows = csv.DictReader(csv_file)
        data = list(rows)
        # Create list with names of every DNA STR
        field_names = rows.fieldnames[1:]

    # Read .txt file and create string variable
    with open(argv[2]) as txt_file:
        dna = txt_file.read()

    # Dictionary of occurrences for every dna STR
    occurrences = {}
    for dna_str in field_names:
        occurrences[dna_str] = longest_match(dna, dna_str)

    # Dictionary of people, where key is a person's name and value is
    # a dictionary of key/value pairs with every DNA STR as a key
    people = {}
    for row in data:
        people[row['name']] = {}
        for dna_str in field_names:
            people[row['name']][dna_str] = row[dna_str]

    # Check number of occurrences of every STR per personw
    for name in people:
        field_names_length = len(field_names) - 1
        for index, DNA_STR in enumerate(field_names):
            if int(people[name][DNA_STR]) != occurrences[DNA_STR]:
                break
            if index == field_names_length:
                return print(name)

    print('No match')
    return


def check_dna_str(val1, val2):
    if val1 == val2:
        return True
    return False


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
